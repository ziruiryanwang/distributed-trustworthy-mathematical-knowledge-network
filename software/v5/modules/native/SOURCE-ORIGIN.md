# Native checker source origin

2026-10-07. Root explicitly selected this bounded copy. Before any edits, all
24 files below were copied byte-for-byte from
`experiments/native-relation-01/project/checker` to
`software/v5/modules/native/checker`; each destination SHA-256 was compared
with its source and matched. No target, cache, binary, `.git`, test-resource
fixture or runtime was copied. Apache-2.0 LICENSE and Cargo.lock are retained.
Subsequent edits are new mutable v5 work; these hashes identify the predecessor,
not current post-edit source or a compiled artifact. No build/test has run.

| Relative source | SHA-256 before edits |
|---|---|
| src/debug_printer.rs | 184918c06946c0efcc57868e47098428bd1d98179725344ba81b1103eb940c81 |
| src/env.rs | 52c1593f0e08c4e7b9b9f8a97e48bfdde1d449253bf0c3e4967321b46dbece01 |
| src/expr.rs | 7ea1a70e11c7adf1fa2f4be8e8a2f10f7fcd6441d73117fdc206a55ac2d76e3c |
| src/inductive.rs | e4be60335f8c0eda18eae074acbf1ea6a6a2b709b31d4d50dbb92dd3443263fc |
| src/level.rs | aaf68c6bb4af87fc026f8560df90c5576abb86e8c59c530aa671465912a998bf |
| src/lib.rs | 23074a173a2ce6c3ca6ef39c9a8da488c7556f9aa95360a50fec7c154dcbee77 |
| src/main.rs | 245ceaef34e8925cacaa3c5b99ce096a8c744710ce1f9184423e5a0333e8b35a |
| src/name.rs | 0e5ea2028ff4d87cc39100d49120f4b08113597d39eb3e916c66ca3c06427478 |
| src/parser.rs | 2bcf40347dfd64832058b3765c40e194e63dae1274284377459626797906b127 |
| src/pretty_printer.rs | 9e45e1951d06d84631d0fee1fdcef60161a757abef53d428625257a0fbe6deb3 |
| src/quot.rs | 0131ae36f3daea5262f280aca44085c15e5335a8657cefd2afcec4c2bc388463 |
| src/tc.rs | 522134805c82cb7522aafc2550a3bfc520455f44f893fb18a94acec5fb162c6f |
| src/tests.rs | 8af730f36984da57fe8ef62818cf3d83c993ed44d1452abc028cc16fcf952f0e |
| src/union_find.rs | 2728ab1d2dcd84489a6bb4fa984af22c40236bf813205e42a1c55ca825bdc757 |
| src/unique_hasher.rs | e457ec69139dee08c4f21f3fee5bc9a2cfe6bb14e5d5bd217ca35d6a368daea5 |
| src/util.rs | 57b2022b743ad5f31cc08d18dfa5092f2246b6a57b2b49770deb0f53cd3e7561 |
| src/tests/level.rs | 5d9c48216082dceab5e278f4121ec9176810d396d29846acb369b3cdc0a80a6f |
| src/tests/name.rs | 7dcb2127f912651f31d47d081f72b2a5cbd98f57d17569db4379733178ed1157 |
| src/tests/natlit.rs | 4710e7daaf796cf32d95da75275d9c536e25ca4e7e43eb003d800e67c16bb2d7 |
| src/tests/pretty_printer.rs | eb93ca77fc48bd095ecfa2719ad8c5b1bf861d1c5bdce585e1b460de3eb301a4 |
| src/tests/util.rs | 9f5a03206d50ec092a26a6d7f3f1b79978b9a978cc977447c0572e0285f6850d |
| Cargo.toml | 0a17b333776ee3f363ba7a51f47e421dc69f93662d5e131870a9d6d95fa9e5d7 |
| Cargo.lock | 9b921e794ce5ed515eb31db9ada0c2f34df999b6c9b5135ad308a412872e42be |
| LICENSE | c8858a5a76440bbca484e134cf7df46385d090dd18b2c58e650f939258802e5b |

Legacy checker tests referring to omitted filesystem fixtures are not automatically
available. The selected new native controls must supply their own exact inputs;
copying old test source does not claim that its campaigns were rerun.
