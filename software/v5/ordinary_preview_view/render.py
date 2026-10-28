"""Bounded, advisory display of one portable preview; no runtime or owner imports.

The caller supplies its selected portable_preview and ordinary_evidence modules.
Malformed preview bytes raise through the existing codec. A display limit returns
an explicit incomplete result with no partial declaration or partial legends.
"""
from __future__ import annotations

import hashlib


DEFAULT_LIMITS = {
    "expression_occurrences": 16384,
    "universe_occurrences": 8192,
    "binder_tokens": 4096,
    "frame_operations": 262144,
    "live_frames": 16384,
    "source_steps": 131072,
    "scope_steps": 65536,
    "temporary_items": 16384,
    "decoded_bytes": 131072,
    "escaped_characters": 131072,
    "name_components": 16384,
    "output_bytes": 65536,
}
ASSURANCE = "ADVISORY_FORMAL_DISPLAY_NOT_MATHEMATICAL_ACCEPTANCE"


class _DisplayStop(Exception):
    def __init__(self, code, **details):
        super().__init__(code)
        self.details = {"code": code, **details}


def _limits(selected):
    if selected is None:
        return dict(DEFAULT_LIMITS)
    if type(selected) is not dict or set(selected) - set(DEFAULT_LIMITS):
        raise ValueError("DISPLAY_LIMIT_FIELDS")
    result = dict(DEFAULT_LIMITS)
    for key, value in selected.items():
        if type(value) is not int or not 1 <= value <= DEFAULT_LIMITS[key]:
            raise ValueError("DISPLAY_LIMIT_VALUE:" + key)
        result[key] = value
    return result


class _Budget:
    def __init__(self, limits):
        self.limits = limits
        self.used = {key: 0 for key in limits}

    def charge(self, key, amount=1):
        if amount < 0 or amount > self.limits[key] - self.used[key]:
            raise _DisplayStop("DISPLAY_LIMIT", counter=key,
                               limit=self.limits[key], charged=self.used[key])
        self.used[key] += amount

    def live(self, amount):
        if amount > self.limits["live_frames"]:
            raise _DisplayStop("DISPLAY_LIMIT", counter="live_frames",
                               limit=self.limits["live_frames"],
                               charged=self.used["live_frames"])
        self.used["live_frames"] = max(self.used["live_frames"], amount)


class _View:
    def __init__(self, doc, evidence, budget):
        self.doc, self.evidence, self.budget = doc, evidence, budget
        self.kind, self.parameters, packet = doc["header"]
        _, self.levels, self.nodes, self.root = packet
        self.fragments, self.frames, self.binders = [], [], []
        self.symbols = doc["type_bindings"]
        self.symbol_keys, self.symbol_tokens = {}, []
        self.parameter_tokens, self.node_symbols = [], {}

    def emit(self, text):
        # All callers construct only already bounded ASCII fragments.
        if not text.isascii():
            raise _DisplayStop("DISPLAY_INTERNAL_NONASCII")
        self.budget.charge("output_bytes", len(text))
        if text:
            self.fragments.append(text)

    def utf8(self, value):
        raw = value["$bytes"]
        self.budget.charge("decoded_bytes", len(raw))
        return bytes(raw).decode("utf-8")

    def hint(self, name, fallback):
        parts = []
        for tag, value in name:
            self.budget.charge("name_components")
            if tag != 0:
                return fallback
            text = self.utf8(value)
            self.budget.charge("source_steps", len(text))
            if (not text or not (text[0].isascii() and
                    (text[0].isalpha() or text[0] == "_")) or
                    any(not (ch.isascii() and (ch.isalnum() or ch == "_"))
                        for ch in text[1:])):
                return fallback
            parts.append(text)
        return ".".join(parts) if parts else fallback

    def escaped(self, text):
        self.emit('"')
        for char in text:
            self.budget.charge("escaped_characters")
            code = ord(char)
            if char == '"':
                self.emit('\\"')
            elif char == "\\":
                self.emit("\\\\")
            elif 0x20 <= code <= 0x7e:
                self.emit(char)
            elif code <= 0xffff:
                self.emit("\\u%04x" % code)
            else:
                code -= 0x10000
                self.emit("\\u%04x\\u%04x" %
                          (0xd800 + (code >> 10), 0xdc00 + (code & 1023)))
        self.emit('"')

    def name(self, name):
        if not name:
            self.emit("[]")
            return
        for index, (tag, value) in enumerate(name):
            self.budget.charge("name_components")
            if index:
                self.emit(" / ")
            if tag == 0:
                self.emit("str(")
                self.escaped(self.utf8(value))
                self.emit(")")
            else:
                self.emit("num(" + str(value) + ")")

    def prepare(self):
        # One exact-key projection per encoded binding/reference, not per
        # occurrence of an exponentially expanded expression.
        for index, (name, _) in enumerate(self.symbols):
            self.budget.charge("source_steps")
            key = self.evidence.name_key(name)
            self.symbol_keys[key] = index
            self.symbol_tokens.append(self.hint(name, "symbol") + "#c" + str(index))
        for index, name in enumerate(self.parameters):
            self.budget.charge("source_steps")
            self.parameter_tokens.append(self.hint(name, "universe") + "#u" + str(index))
        for index, node in enumerate(self.nodes):
            self.budget.charge("source_steps")
            if node[0] in (2, 8):
                key = self.evidence.name_key(node[1])
                if key not in self.symbol_keys:
                    raise _DisplayStop("DISPLAY_REFERENCE_UNAVAILABLE", node=index)
                self.node_symbols[index] = self.symbol_keys[key]

    def push(self, *frame):
        self.budget.charge("frame_operations")
        self.budget.live(len(self.frames) + 1)
        self.frames.append(frame)

    def variable(self, environment, distance):
        current = environment
        for _ in range(distance):
            self.budget.charge("scope_steps")
            if current is None:
                raise _DisplayStop("DISPLAY_SCOPE_UNAVAILABLE")
            current = current[1]
        self.budget.charge("scope_steps")
        if current is None:
            raise _DisplayStop("DISPLAY_SCOPE_UNAVAILABLE")
        return current[0]

    def binder(self, index, node):
        self.budget.charge("binder_tokens")
        token = self.hint(node[1], "arg") + "#b" + str(len(self.binders))
        self.binders.append((token, index, node[1], node[0],
                             node[2] if node[0] in (4, 5) else node[5]))
        return token

    def level(self, index):
        self.budget.charge("universe_occurrences")
        node = self.levels[index]
        tag = node[0]
        if tag == 0:
            self.emit("zero")
        elif tag == 4:
            self.emit(self.parameter_tokens[node[1]])
        elif tag == 1:
            self.emit("succ(")
            self.push("text", ")")
            self.push("level", node[1])
        elif tag in (2, 3):
            self.emit("max(" if tag == 2 else "imax(")
            self.push("text", ")")
            self.push("level", node[2])
            self.push("text", ",")
            self.push("level", node[1])
        else:
            raise _DisplayStop("DISPLAY_UNSUPPORTED_LEVEL", tag=tag)

    def expression(self, index, environment, top):
        self.budget.charge("expression_occurrences")
        node = self.nodes[index]
        tag = node[0]
        if tag == 0:
            self.emit(self.variable(environment, node[1]))
        elif tag == 1:
            self.emit("Sort(")
            self.push("text", ")")
            self.push("level", node[1])
        elif tag == 2:
            self.emit(self.symbol_tokens[self.node_symbols[index]])
            if node[2]:
                self.emit(".{")
                self.push("text", "}")
                for position in range(len(node[2]) - 1, -1, -1):
                    self.push("level", node[2][position])
                    if position:
                        self.push("text", ",")
        elif tag == 3:
            # Flatten only the application spine, with the same environment.
            # Charge each additional application before following its children.
            arguments = []
            current = index
            while self.nodes[current][0] == 3:
                self.budget.charge("temporary_items")
                arguments.append(self.nodes[current][2])
                current = self.nodes[current][1]
                if self.nodes[current][0] == 3:
                    self.budget.charge("expression_occurrences")
            self.emit("(")
            self.push("text", ")")
            for argument in arguments:
                self.push("expr", argument, environment, False)
                self.push("text", " ")
            self.push("expr", current, environment, False)
        elif tag in (4, 5):
            token = self.binder(index, node)
            next_environment = (token, environment)
            left, right = (("(", ")"), ("{", "}"),
                           ("{{", "}}"), ("[", "]"))[node[2]]
            outer = top and tag == 5
            self.emit(("forall " if outer else "(forall ") if tag == 5 else "(fun ")
            if not outer:
                self.push("text", ")")
            self.push("expr", node[4], next_environment, outer)
            self.push("text", ",\n" if outer else (", " if tag == 5 else " => "))
            self.push("text", right)
            self.push("expr", node[3], environment, False)
            self.push("text", left + token + " : ")
        elif tag == 6:
            token = self.binder(index, node)
            next_environment = (token, environment)
            self.emit("(let[nondep=" + str(node[5]) + "] (" + token + " : ")
            self.push("text", ")")
            self.push("expr", node[4], next_environment, False)
            self.push("text", " in ")
            self.push("expr", node[3], environment, False)
            self.push("text", ") := ")
            self.push("expr", node[2], environment, False)
        elif tag == 7:
            raw = node[1]["$bytes"]
            self.budget.charge("decoded_bytes", len(raw))
            self.emit("nat[be:0x")
            if not raw:
                self.emit(";zero")
            for byte in raw:
                self.budget.charge("escaped_characters")
                self.emit("%02x" % byte)
            self.emit("]")
        elif tag == 8:
            self.emit("(proj " + self.symbol_tokens[self.node_symbols[index]] +
                      " field=" + str(node[2]) + " ")
            self.push("text", ")")
            self.push("expr", node[3], environment, False)
        elif tag == 9:
            self.emit("string(")
            self.escaped(self.utf8(node[1]))
            self.emit(")")
        else:
            raise _DisplayStop("DISPLAY_UNSUPPORTED_EXPRESSION", tag=tag)

    def render_type(self):
        self.push("expr", self.root, None, True)
        while self.frames:
            self.budget.charge("frame_operations")
            frame = self.frames.pop()
            if frame[0] == "text":
                self.emit(frame[1])
            elif frame[0] == "level":
                self.level(frame[1])
            else:
                self.expression(frame[1], frame[2], frame[3])

    def run(self):
        self.prepare()
        self.emit("ADVISORY CLAIM; no mathematical acceptance.\n")
        self.emit("Kind code: " + str(self.kind) + "; root: e" + str(self.root) + "\n")
        self.emit("Declaration exact name: ")
        self.name(self.doc["export_name"])
        self.emit("\nUniverse parameters (original order): [")
        for index, token in enumerate(self.parameter_tokens):
            self.budget.charge("source_steps")
            if index:
                self.emit(", ")
            self.emit(token)
        self.emit("]\n\nTYPE (complete):\n")
        self.render_type()
        self.emit("\n\nSYMBOLS (binding index, exact name, SymbolID):\n")
        for index, (name, symbol) in enumerate(self.symbols):
            self.budget.charge("source_steps")
            self.emit(self.symbol_tokens[index] + " | ")
            self.name(name)
            self.emit(" | " + symbol + "\n")
        self.emit("\nBINDERS (occurrence, source node, original exact label, information):\n")
        for token, index, name, tag, information in self.binders:
            self.budget.charge("source_steps")
            self.emit(token + " | e" + str(index) + " | ")
            self.name(name)
            self.emit((" | nondep=" if tag == 6 else " | binder_info=") +
                      str(information) + "\n")
        self.emit("\nUNIVERSE PARAMETERS (position, exact name):\n")
        for index, name in enumerate(self.parameters):
            self.budget.charge("source_steps")
            self.emit(self.parameter_tokens[index] + " | ")
            self.name(name)
            self.emit("\n")
        self.emit("\nLegend: #c=exact binding row; #b=fresh scoped binder occurrence; "
                  "#u=original universe position.\n"
                  "No universe suffix means an empty universe argument list.\n"
                  "Binder info 0=(default), 1={implicit}, 2={{strictImplicit}}, "
                  "3=[instImplicit].\n"
                  "nat[be:0x;zero] is the empty zero magnitude; other Nat magnitudes "
                  "are exact big-endian hex.\n"
                  "SymbolID is not necessarily an ordinary ExportID or an "
                  "inspectable unit. Display syntax is not compilable Lean source.\n")
        return "".join(self.fragments)


def render_preview(raw, *, codec, evidence, limits=None):
    """Return one complete ASCII view or an explicit, detached incomplete result.

    ``codec`` is the selected portable_preview module; ``evidence`` is its
    selected ordinary_evidence module. Only those codecs parse/validate input.
    ``limits`` may lower known defaults. No report provenance is accepted here.
    Invalid configuration/preview bytes raise; display limits never renew.
    """
    selected = _limits(limits)
    if type(raw) is not bytes:
        raise ValueError("DISPLAY_RAW_PREVIEW_BYTES_REQUIRED")
    preview = codec.read_preview(raw)
    doc = preview.document
    budget = _Budget(selected)
    result = {
        "status": "TYPE_DISPLAY_INCOMPLETE", "complete": False,
        "view_text": None, "semantic_id": doc["semantic_id"],
        "unit_id": doc["unit_id"], "export_id": preview.export_id,
        "preview_sha256": hashlib.sha256(raw).hexdigest(),
        "preview_bytes": len(raw), "root_node": doc["header"][2][3],
        "kind_code": doc["header"][0], "limits": dict(selected),
        "counters": None, "limitation": None,
        "mathematical_acceptance": False, "assurance": ASSURANCE,
    }
    try:
        text = _View(doc, evidence, budget).run()
    except _DisplayStop as stopped:
        result["limitation"] = dict(stopped.details)
    else:
        result.update(status="TYPE_DISPLAY_COMPLETE", complete=True, view_text=text)
    result["counters"] = dict(budget.used)
    return result
