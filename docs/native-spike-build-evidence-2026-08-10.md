# Native spike build evidence — 2026-08-10

## Classification

`minimal-dual-host-proven / declared-composition-and-basecamp-dual-host-proven / corrected-policy-and-reference-gates-pending`

The source and gate at commit
`0fc38dc02dcc91fc0c786dce006ee9511d922c7d` completed the public contract
and native-spike workflows on Ubuntu 24.04 and macOS 15. Run
[`31404402665`](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665)
then proved the same portable package through the real Basecamp 0.2.3 Module
Inspector on both hosts, including method/event discovery, calls, unload, and
reload. It does not prove protocol composition, capability-policy parity,
testnet deployment, or prize readiness.

Commit `d2179730227ec0641d11909baa71f3b9a1d35194` then proved exact
Chat 0.2.2 and transitive Delivery 0.2.0 composition through generated typed
glue on both headless hosts. Both native jobs ended red only because the first
policy assertion incorrectly expected the trusted `core_service` administrative
path to behave like a peer capability request. The same composed package also
passed the exact Basecamp path on both hosts, including the explicit Linux
dynamic closure.

## Public evidence

- Pull request: [#1](https://github.com/Devpen787/logos-sovereign-agent/pull/1)
- Contract workflow: [run 31395410117](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410117)
- Native runtime workflow: [run 31395410267](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267)
- Linux job: [93476957618](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957618)
- macOS job: [93476957501](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957501)
- Linux evidence artifact: [9065899299](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065899299), retained through 2026-09-09
- macOS evidence artifact: [9065876532](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065876532), retained through 2026-09-09
- Basecamp workflow: [run 31404402665](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665)
- Basecamp Linux job: [93507057966](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/job/93507057966)
- Basecamp macOS job: [93507057950](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/job/93507057950)
- Basecamp Linux artifact: [9069852891](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/artifacts/9069852891), retained through 2026-09-09
- Basecamp macOS artifact: [9070004456](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/artifacts/9070004456), retained through 2026-09-09
- Declared-composition native workflow: [run 31407268662](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268662)
- Composition Linux artifact: [9071379824](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268662/artifacts/9071379824), SHA-256 `81fb509906ad78b8dcb7cbe7d5f4aa6c03a679da76973939756df4834821e093`
- Composition macOS artifact: [9071839374](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268662/artifacts/9071839374), SHA-256 `880c5757557a97435c3dd246c2e3f33dbdc699f3041345db3894de304464acdb`
- Composed Basecamp workflow: [run 31407268710](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268710)
- Composed Basecamp Linux artifact: [9071850377](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268710/artifacts/9071850377), SHA-256 `4560086fe1159342e55e1811feff544765eb6cc82764c3dfc7e04ba787c66611`
- Composed Basecamp macOS artifact: [9072362864](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268710/artifacts/9072362864), SHA-256 `d5ddb2f2fe6bb5cebc93aaf35ff00b83f30487d870b47d4d8f14e51cb81e9d1a`

## Exact output identities

The generated dependency lock has SHA-256
`5d25b56a124cb93601c8b203d703da5946137bdd8e4a857c3110f169a86db7f2`
on both hosts.

| Host | Variant | LGX SHA-256 |
|---|---|---|
| Ubuntu 24.04 | development, `linux-amd64-dev` | `fae8f8a80d4562387e12be640de8351ae8fe4a4640426da231edd8a0b542d86b` |
| Ubuntu 24.04 | portable, `linux-amd64` | `bf4fe21b9066bbfe79638985ee5c4e1d9832399e55a4a8f9e9d836461c548360` |
| macOS 15 | development, `darwin-arm64-dev` | `fd4bf28fd64c22d085e27e3b0cbe53f2dbb1bcc141334751d510d92de94b2966` |
| macOS 15 | portable, `darwin-arm64` | `431a0143007f714bf78ebbf127eadf823c8ce19a6d1964440b9df11472ecca10` |

Each output contains `logos-sovereign_agent-module-lib.lgx`.

The declared-composition root lock is byte-identical in the Ubuntu and macOS
headless and Basecamp artifacts, with SHA-256
`201fd38cfb5d5cfd5f4a5fe0d71470f92e5d8816555a0b57ced94891ca1ef84a`.
It is committed in the next candidate so the workflow must prove `nix flake
lock` leaves it unchanged.

| Host | Variant | NAR hash | LGX SHA-256 |
|---|---|---|---|
| Ubuntu 24.04 | development | `sha256-gGmAeBxsDaOQsuQsqNopIbo/FDBr844PpJogVhv3C6o=` | `439a34cfb1f49414d69607d2be04fa2900528cf4fe6a5b095eccf852352483b6` |
| Ubuntu 24.04 | portable | `sha256-NULDvR/zDXGDrmOoS/rp2RoPJngkXC1BWGwdROM56p4=` | `d2a45fc8d1166c30509cbfc056ab95db78814f1a53c683bfa671131de1572d33` |
| macOS 15 | development | `sha256-yfP5naErO28VZS6dokDOIsPdeOLUoAge021UAdnnsjM=` | `027b72c5db15d2322742a2516058c71a2ec4d6724eefa5ae781a19bb7c9f6da6` |
| macOS 15 | portable | `sha256-fuPo9l2njtUKzDlIjj1pvVLIOKyglSk4h+nzLa7PO9I=` | `ce2f134c99b451389745a27eb39195dda9a9e7d43891c493c25792f0903575c8` |

Each composed Basecamp artifact contains the same portable LGX SHA-256 as its
headless host. The Ubuntu screenshot SHA-256 is
`1ed96807297693bd8678475ee51b8bb335a698dcf66e95320622627fd1380c36`; the
macOS screenshot SHA-256 is
`2a71d5a52075102941f20f00da4f6117f48b26db564da7476c99100f189074ab`.

An earlier revision mislabeled values from `nix hash path` over the result
links as the NAR identities of the two outputs. Those four claims are
withdrawn. Commit `d828039b72c9ccefd6cfd901256bd4e3cc2e0770` changes the
collector to use `nix path-info --json` and fails the job unless both output
records contain a `narHash`. No replacement NAR values are claimed here until
the collector emits an explicit development/portable mapping. Run
[`31404402750`](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402750)
contains two valid `narHash` records per host, but the unlabeled pair is not
being mapped by path order or inferred size.

## Runtime assertions

Both host jobs proved all of the following against exact pinned releases:

- unsigned development-package installation with `lgpm` 0.2.1 source commit
  `202af6fa0f0f4493bc59c8a609dff9326f78a18d`;
- daemon startup with the bundled capability module;
- discovery before load and `loaded` state after load;
- method and event introspection for `version`, `status`, and `statusChanged`;
- deterministic calls before and after reload;
- process statistics while loaded; and
- clean stop followed by `daemon.status == not_running`.

## Disclosed findings

The composed Basecamp run proves runtime viability on both hosts and captures
an explicit Linux `ldd` closure with no unresolved libraries. macOS does not
have an equivalent `ldd` assertion.

Exact Basecamp 0.2.3 calls `logos_core_set_access_policy(nullptr)` and explains
that policy enforcement is temporarily disabled because QML callers are not
represented in the module dependency graph. The frozen Logos Core flake,
despite stale README/source comments saying policy is a no-op, resolves its
root `logos-liblogos_8` input to commit
`be221c5749036343909fa0b109edecfb4d329fdd`, which implements parsed enforce
policies and derived caller restrictions. Capability denial therefore must be
proved in the headless lane and disclosed as non-equivalent in Basecamp.

Candidate run
[`31407268662`](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31407268662)
proved that the declared typed `sovereign_agent -> chat_module` health call
returns `true`, but it also falsified the initial assumption that an
administrative `core_service -> chat_module` CLI call should be denied. The
core-service call returned `true`. The corrected gate tests the capability
module's actual peer-token boundary instead: a loaded but unlisted
`delivery_module` requesting a Chat token must receive an empty token, while
the core-service result is retained as a separate administrative-path record.

The Basecamp logs expose process-local UUID tokens while the runtime is alive.
They are invalid after process exit, but future evidence collectors redact all
UUID-shaped values from captured `.log` and `.txt` files before upload. The two
already-published minimal-contract artifacts are retained as historical
evidence and are not described as sanitized.

The macOS portable bundler reported embedded `/nix/` strings in the module and
OpenSSL binary data, then classified all references as portable. The module
has not yet been run outside Nix, so this remains an explicit portability risk
rather than a closed finding.

The macOS daemon also logged a missing `eventResponse(QString, QVariantList)`
signal while initializing Logos Core's bundled capability module. The
sovereign-agent provider loaded, forwarded its own event, reloaded, and stopped
successfully. The warning is retained as upstream host evidence.

The first runtime-gate run correctly produced all successful lifecycle records
but ended red because the verifier assumed post-stop `status` must exit
non-zero. Pinned Logos Core returned the correct `not_running` JSON with exit
code zero. Commit `0fc38dc` changed the gate to assert the returned state; the
fresh two-host run is green.

GitHub currently warns that the pinned latest `actions/upload-artifact` v7.0.1
action declares Node.js 20 while the runner forces Node.js 24. Artifact upload
completed on both hosts. This is a CI-maintenance warning, not module evidence.

## Next gate

Prove the corrected capability-module peer-token denial, compile-time
undeclared-dependency rejection, runtime missing-dependency rejection, and
unmodified official Chat/LEZ reference specifications. Commit the generated
dependency lock and make every uploaded artifact pass the independent
fail-closed auditor. No product feature work begins from this partial result
alone.
