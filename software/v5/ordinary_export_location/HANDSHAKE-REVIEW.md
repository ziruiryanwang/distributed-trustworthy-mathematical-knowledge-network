# Original operator horizon: independent supplemental review

2026-10-28, growth_design_audit. **PASS for the startup-handshake source delta.**
No product code, Node process, database or network was executed. Preserve the
earlier `BACKEND-REVIEW.md`; this note supplements its replaced lifetime/startup
boundary rather than changing its frozen reviewed identities.

Reviewed controller
`0b7846e3936e6120d7d227e438d700e85b812139054808824dac2da503437b3d`,
maintained roles
`0bf7a1befa76228c71a45e9fa80f1c0c0abd00ca3ba3dcb9084678b39f901744`,
Node entry
`086936eac4cf9444e20bd4c485777aaa9a3ea277a000d0aeef703d633104d43e`,
wire contract
`52c69655bf8b8318ff5bb6f280f8bf93997f1aa601daf6b324c4ddf53742e12b`,
and updated backend checkpoint
`e9663ec13ff9e179c0ca9f67b183c44bfaa034287d8e565b1fcda39c19ba02a8`.

The previous composition let the child start its full service duration after
parent runtime verification/setup, although the wrapper's service clock had
already started. Later wrapper shutdown did not make the child's larger advertised
remaining duration conservative. The new protocol resolves that specific issue.

Node records a local marker before emitting PREPARED and before store/network
effects. Only after receiving PREPARED does Python compute remaining durations
from its original service and channel cutoffs and send BEGIN. Node anchors both
durations at its earlier marker, clips them to its own initial finite ceilings,
and passes the resulting service cutoff to `MaintainedLocator.start`. Subsequent
runtime loading, store initialization, census and network startup consume that
same cutoff. Descriptor production continues to use `locator.until`.

With ordinary monotonic-clock rate accuracy, let a be the real time of Node's
marker, b the later time when Python computes the remaining service duration,
and T the original parent cutoff. The sent duration r is at most T-b. The child
cutoff is at most a+r, hence at most T-(b-a) <= T. No absolute clock-origin
comparison is required. Rounding down and all later clipping only shorten this
horizon. The same argument applies to private-channel authority. Transit and
startup cannot renew either grant. This is not a Byzantine-clock guarantee.

Service shutdown and private-pipe shutdown are now separate. Routing/renewal
stops at the service cutoff; status and stop remain possible under the separate
bounded channel cutoff. Python restricts substantive commands to its original
service deadline and uses its original channel deadline for finalization. An
expired or malformed handshake uses the existing terminal drain path; no second
startup grant is offered.

PREPARED and READY consume the two reply lifecycle frames already allowed by
the C+2 frame ceiling. BEGIN adds one charged input frame, leaving input frames
at most C+1. Its bytes are counted by both sides; subsequent command admission
uses counters including the handshake and still reserves finalization capacity.
The configured byte/frame ceilings are unchanged. Same-config reopen identity
does not contain transient cutoff values; only the explicit launch grant changes.

No new blocker was found. A small scripted startup exchange can later check
PREPARED binding, consumed startup time and failure cleanup; a new proof or
certificate campaign would be irrelevant.
