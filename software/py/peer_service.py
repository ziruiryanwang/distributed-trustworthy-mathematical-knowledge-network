"""Finite read-only loopback HTTP and inert acquisition. No acceptance authority."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import time

import peer_wire as W

HEADER_MAX = 8192
LINE_MAX = 2048
SESSION_SECONDS = 600
SESSION_CPU = 120
SESSION_REQUESTS = 128
SESSION_BYTES = 256 * W.MIB
TRANSFER_SECONDS = 30
IDLE_SECONDS = 5


def _port(value, zero=False):
    W.require(type(value) is int and (0 if zero else 1) <= value <= 65535, "LOCAL_ENDPOINT_REFUSED")
    return value


def _timeout(sock, deadline):
    remaining = deadline - time.monotonic()
    W.require(remaining > 0, "TRANSFER_TIMEOUT")
    sock.settimeout(min(IDLE_SECONDS, remaining))


def _recv(sock, amount, deadline):
    _timeout(sock, deadline)
    try:
        return sock.recv(amount)
    except socket.timeout:
        raise W.WireError("TRANSFER_TIMEOUT") from None
    except OSError:
        raise W.WireError("PEER_UNAVAILABLE") from None


def _send(sock, raw, deadline, cpu_deadline=None):
    sent = 0
    while sent < len(raw):
        _timeout(sock, deadline)
        if cpu_deadline is not None:
            W.require(time.process_time() <= cpu_deadline, "LOCAL_QUOTA")
        try:
            count = sock.send(raw[sent:sent + 65536])
        except socket.timeout:
            raise W.WireError("TRANSFER_TIMEOUT") from None
        except OSError:
            raise W.WireError("PEER_UNAVAILABLE") from None
        W.require(count > 0, "PEER_UNAVAILABLE")
        sent += count
    return sent


def _head(sock, deadline, observations=None):
    raw = bytearray()
    while True:
        end = raw.find(b"\r\n\r\n")
        if end >= 0:
            W.require(end + 4 <= HEADER_MAX, "HTTP_PROFILE_REFUSED")
            head, remaining = bytes(raw[:end]), bytes(raw[end + 4:])
            break
        W.require(len(raw) < HEADER_MAX, "HTTP_PROFILE_REFUSED")
        chunk = _recv(sock, min(1024, HEADER_MAX - len(raw)), deadline)
        W.require(chunk, "HTTP_PROFILE_REFUSED")
        if observations is not None:
            observations["received_bytes"] += len(chunk)
        raw.extend(chunk)
    lines = head.split(b"\r\n")
    W.require(lines and 0 < len(lines[0]) <= LINE_MAX and all(32 <= c <= 126 for c in lines[0]),
              "HTTP_PROFILE_REFUSED")
    headers = {}
    for line in lines[1:]:
        W.require(b":" in line and not line.startswith((b" ", b"\t")), "HTTP_PROFILE_REFUSED")
        key, value = line.split(b":", 1)
        W.require(key and all(c in b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in key),
                  "HTTP_PROFILE_REFUSED")
        key = key.lower()
        value = value.strip(b" \t")
        W.require(key not in headers and all(32 <= c <= 126 for c in value), "HTTP_PROFILE_REFUSED")
        headers[key] = value
    return lines[0], headers, remaining


class _SocketStream:
    def __init__(self, sock, deadline, initial=b""):
        self.sock, self.deadline, self.pending = sock, deadline, initial

    def read(self, count):
        W.require(type(count) is int and 0 <= count <= W.BUNDLE_MAX, "TRANSFER_LIMIT")
        if not count:
            return b""
        if self.pending:
            raw, self.pending = self.pending[:count], self.pending[count:]
            return raw
        return _recv(self.sock, min(count, 65536), self.deadline)


def _get(port, path, maximum, media_type, consume):
    _port(port)
    deadline = time.monotonic() + TRANSFER_SECONDS
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(2)
        try:
            sock.connect(("127.0.0.1", port))
        except socket.timeout:
            raise W.WireError("TRANSFER_TIMEOUT") from None
        except OSError:
            raise W.WireError("PEER_UNAVAILABLE") from None
        request = ("GET " + path + " HTTP/1.1\r\nHost: 127.0.0.1:" + str(port) +
                   "\r\nConnection: close\r\n\r\n").encode("ascii")
        _send(sock, request, deadline)
        first, headers, pending = _head(sock, deadline)
        parts = first.split(b" ", 2)
        W.require(len(parts) == 3 and parts[0] == b"HTTP/1.1" and len(parts[1]) == 3 and parts[1].isdigit(),
                  "HTTP_PROFILE_REFUSED")
        W.require(headers.get(b"connection", b"").lower() == b"close" and
                  b"transfer-encoding" not in headers and b"content-encoding" not in headers and
                  b"location" not in headers, "HTTP_PROFILE_REFUSED")
        length_text = headers.get(b"content-length", b"")
        W.require(length_text.isdigit() and len(length_text) <= 9, "HTTP_PROFILE_REFUSED")
        length = int(length_text)
        W.require(length <= maximum, "TRANSFER_LIMIT")
        W.require(headers.get(b"content-type") == (media_type if parts[1] == b"200" else b"application/json"),
                  "HTTP_PROFILE_REFUSED")
        stream = _SocketStream(sock, deadline, pending)
        if parts[1] != b"200":
            W.require(length <= 4096, "TRANSFER_LIMIT")
            reader = W._BoundedReader(stream, length)
            reader.take(length)
            reader.finish()
            raise W.WireError("PEER_NOT_FOUND" if parts[1] == b"404" else "PEER_UNAVAILABLE")
        return consume(stream, length)
    finally:
        sock.close()


def fetch_catalog(port, foundation):
    def consume(stream, length):
        reader = W._BoundedReader(stream, length)
        raw = reader.take(length)
        reader.finish()
        return {"catalog": W.parse_catalog(raw, foundation), "sha256": W.digest(raw)}
    return _get(port, "/v1/catalog", W.CATALOG_MAX, b"application/json", consume)


def acquire(port, entry, foundation, destination):
    W.validate_entry(entry)

    def consume(stream, length):
        W.require(length == entry["bundle_bytes"], "BUNDLE_FRAMING_REFUSED")
        return W.receive_bundle(stream, entry, foundation, destination)
    return _get(port, "/v1/bundle/" + entry["bundle_sha256"], W.BUNDLE_MAX,
                b"application/octet-stream", consume)


def _response(sock, status, body, media, deadline, observations, byte_limit, cpu_deadline):
    reasons = {200: "OK", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed", 503: "Service Unavailable"}
    header = ("HTTP/1.1 " + str(status) + " " + reasons[status] + "\r\nContent-Length: " + str(len(body)) +
              "\r\nContent-Type: " + media + "\r\nConnection: close\r\n\r\n").encode("ascii")
    # Reserve attempted bytes before IO; partial sends cannot evade the quota.
    charged = len(header) + len(body)
    W.require(observations["charged_send_bytes"] + charged <= byte_limit, "LOCAL_QUOTA")
    observations["charged_send_bytes"] += charged
    observations["completed_send_bytes"] += _send(sock, header, deadline, cpu_deadline)
    for offset in range(0, len(body), 65536):
        observations["completed_send_bytes"] += _send(sock, body[offset:offset + 65536], deadline, cpu_deadline)


def _publish_ready(path, value):
    """Publish a complete readiness file atomically, without replacing a target."""
    path = Path(path).absolute()
    W.safe_path(path.parent, directory=True)
    W.require(not path.exists(), "LOCAL_PATH_REFUSED")
    descriptor, temporary = tempfile.mkstemp(prefix=".peer-ready-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(W.encoded(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)


def serve(view, port, ready=None, *, stop=None, session_seconds=SESSION_SECONDS,
          max_requests=SESSION_REQUESTS, max_bytes=SESSION_BYTES):
    """No OS sandbox here: caller must provide process-tree memory/CPU supervision.

    Optional stop event and stricter session ceilings are owner-local controls.
    This function returns observations and never launches native/checker work.
    """
    _port(port, zero=True)
    for value, maximum in ((session_seconds, SESSION_SECONDS), (max_requests, SESSION_REQUESTS), (max_bytes, SESSION_BYTES)):
        W.require(type(value) is int and 0 < value <= maximum, "LOCAL_QUOTA")
    started, cpu_start = time.monotonic(), time.process_time()
    selected = W.load_view(view)
    deadline, cpu_deadline = started + session_seconds, cpu_start + SESSION_CPU
    result = {"connections": 0, "responses": 0, "received_bytes": 0, "completed_send_bytes": 0,
              "charged_send_bytes": 0, "checker_loaded": False, "native_stages": 0,
              "mathematicalAcceptance": False, "bind_host": "127.0.0.1"}
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        server.bind(("127.0.0.1", port))
        server.listen(1)
        server.settimeout(0.2)
        result["port"] = server.getsockname()[1]
        if ready is not None:
            _publish_ready(ready, {"host": "127.0.0.1", "port": result["port"],
                                   "catalog_sha256": W.digest(selected["catalog_raw"])})
        while result["connections"] < max_requests and result["charged_send_bytes"] < max_bytes:
            if stop is not None and stop.is_set():
                result["stop_reason"] = "OWNER_STOP"
                break
            if time.monotonic() >= deadline or time.process_time() >= cpu_deadline:
                result["stop_reason"] = "SESSION_LIMIT"
                break
            try:
                connection, address = server.accept()
            except socket.timeout:
                continue
            result["connections"] += 1
            with connection:
                request_deadline = min(deadline, time.monotonic() + TRANSFER_SECONDS)
                try:
                    W.require(address[0] == "127.0.0.1", "HTTP_PROFILE_REFUSED")
                    first, headers, pending = _head(connection, request_deadline, result)
                    parts = first.split(b" ")
                    W.require(len(parts) == 3 and parts[2] == b"HTTP/1.1", "HTTP_PROFILE_REFUSED")
                    W.require(set(headers) <= {b"host", b"connection", b"content-length"} and
                              headers.get(b"host") == ("127.0.0.1:" + str(result["port"])).encode() and
                              headers.get(b"connection", b"").lower() == b"close" and
                              headers.get(b"content-length", b"0") == b"0" and not pending, "HTTP_PROFILE_REFUSED")
                    if parts[0] != b"GET":
                        status, body, media = 405, W.encoded({"code": "METHOD_REFUSED"}), "application/json"
                    elif parts[1] == b"/v1/catalog":
                        status, body, media = 200, selected["catalog_raw"], "application/json"
                    elif parts[1].startswith(b"/v1/bundle/"):
                        tail = parts[1][len(b"/v1/bundle/"):]
                        try:
                            key = tail.decode("ascii")
                        except UnicodeError:
                            key = ""
                        if W.HEX.fullmatch(key) and key in selected["bundles"]:
                            path, length = selected["bundles"][key]
                            body = W.read_local(path, W.BUNDLE_MAX)
                            W.require(len(body) == length and W.digest(body) == key, "BUNDLE_DIGEST_MISMATCH")
                            status, media = 200, "application/octet-stream"
                        else:
                            status, body, media = 404, W.encoded({"code": "PEER_NOT_FOUND"}), "application/json"
                    else:
                        status, body, media = 404, W.encoded({"code": "PEER_NOT_FOUND"}), "application/json"
                    _response(connection, status, body, media, request_deadline, result, max_bytes, cpu_deadline)
                    result["responses"] += 1
                except (W.WireError, OSError) as error:
                    result["last_error"] = error.code if isinstance(error, W.WireError) else "LOCAL_IO_FAILURE"
                    # Close on uncertain/partial response. Never append a second reply.
                    continue
        result.setdefault("stop_reason", "SESSION_LIMIT")
    finally:
        server.close()
    result["elapsed_seconds"] = time.monotonic() - started
    result["cpu_seconds"] = time.process_time() - cpu_start
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", required=True, type=Path)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--ready", required=True, type=Path)
    args = parser.parse_args()
    W.require(sys.dont_write_bytecode and sys.flags.ignore_environment and
              sys.flags.no_user_site and sys.flags.no_site, "PYTHON_ISOLATED_PROFILE")
    try:
        result = serve(args.view, args.port, args.ready)
    except (W.WireError, OSError) as error:
        print(json.dumps({"status": "STOPPED", "code": getattr(error, "code", "LOCAL_IO_FAILURE")}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
