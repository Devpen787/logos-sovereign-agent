# Native spike build evidence — 2026-08-10

## Classification

`logoscore-cross-platform-runtime-proven / basecamp-pending`

The source and gate at commit
`0fc38dc02dcc91fc0c786dce006ee9511d922c7d` completed the public contract
and native-spike workflows on Ubuntu 24.04 and macOS 15. This proves the
minimal module contract in pinned Logos Core 0.2.2. It does not prove Basecamp,
real protocol composition, testnet deployment, or prize readiness.

## Public evidence

- Pull request: [#1](https://github.com/Devpen787/logos-sovereign-agent/pull/1)
- Contract workflow: [run 31395410117](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410117)
- Native runtime workflow: [run 31395410267](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267)
- Linux job: [93476957618](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957618)
- macOS job: [93476957501](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957501)
- Linux evidence artifact: [9065899299](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065899299), retained through 2026-09-09
- macOS evidence artifact: [9065876532](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065876532), retained through 2026-09-09

## Exact output identities

The generated dependency lock has SHA-256
`5d25b56a124cb93601c8b203d703da5946137bdd8e4a857c3110f169a86db7f2`
on both hosts.

| Host | Variant | LGX SHA-256 | NAR hash |
|---|---|---|---|
| Ubuntu 24.04 | development, `linux-amd64-dev` | `fae8f8a80d4562387e12be640de8351ae8fe4a4640426da231edd8a0b542d86b` | `sha256-BDMWB36i0s5vdh0GoPMVsaEoGNS31sv8zhUdQRTk1Xk=` |
| Ubuntu 24.04 | portable, `linux-amd64` | `bf4fe21b9066bbfe79638985ee5c4e1d9832399e55a4a8f9e9d836461c548360` | `sha256-UcQ71mnO//m3hnXl1nlo0hxJu6aRX85tJLZopcfRBkA=` |
| macOS 15 | development, `darwin-arm64-dev` | `fd4bf28fd64c22d085e27e3b0cbe53f2dbb1bcc141334751d510d92de94b2966` | `sha256-yip3ogq+MWhThUe0aFOmFKUZ7K6no81HZrHLLfzHOrc=` |
| macOS 15 | portable, `darwin-arm64` | `431a0143007f714bf78ebbf127eadf823c8ce19a6d1964440b9df11472ecca10` | `sha256-uWp+CwjIAR4rgOsi9hRazHUaEiTuPQDKCIf19/H8zFA=` |

Each output contains `logos-sovereign_agent-module-lib.lgx`.

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

Prove the same package contract without official-source modification in
Basecamp 0.2.3, then close the remaining package-negative and clean-checkout
items in the bounded native-spike packet. No protocol feature work begins from
this result alone.
