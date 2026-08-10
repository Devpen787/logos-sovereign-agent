# Native spike build evidence — 2026-08-10

## Classification

`cross-platform-build-proven / runtime-load-pending`

The source at commit `c3556bbdf8eddb58645e3687dac842543b445b67`
completed the public contract and native build workflows. This proves package
construction, not runtime compatibility or prize readiness.

## Public evidence

- Contract workflow: [run 31393630946](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31393630946)
- Native build workflow: [run 31393631176](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31393631176)
- Linux job: [93471088671](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31393631176/job/93471088671)
- macOS job: [93471088704](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31393631176/job/93471088704)

## Exact output identities

| Host | Variant | NAR hash |
|---|---|---|
| Ubuntu 24.04 | development, `linux-amd64-dev` | `sha256-hHADNcm3qnf0yk3DLssYH3nRhUzS/YtgKqWoo8hpwQg=` |
| Ubuntu 24.04 | portable, `linux-amd64` | `sha256-FBtyWK4wZAWbcF0jQwAUeIuuWBQMJDlV4eTitIi/s7o=` |
| macOS 15 | development, `darwin-arm64-dev` | `sha256-3Qo1dIZLyZsNc7rNOwIiOTOZG3WBiMOqllHI7N5Ew0s=` |
| macOS 15 | portable, `darwin-arm64` | `sha256-+CQdQ5Vt+MfMIQxQFuT/N+jHXvbLrHVCS+TihGYOG58=` |

Each output contains `logos-sovereign_agent-module-lib.lgx`.

## Disclosed finding

The macOS portable bundler reported embedded `/nix/` strings in the module and
OpenSSL binary data, then classified all references as portable. The module
has not yet been run outside Nix, so this remains an explicit portability risk
rather than a closed finding.

## Next gate

The workflow now generates a dependency lock, uploads the `.lgx` artifacts and
evidence manifests, installs the development package with the pinned package
manager, and exercises discovery, load, introspection, calls, stats, reload,
stop, and post-stop state through the pinned Logos Core CLI on both platforms.
