# Logos Sovereign Agent Instructions

## Mission

Build the native LP-0008 Logos Core module. Every claim must identify its
evidence class: planned, local, native-runtime, clean-clone, testnet, public,
submitted, accepted, or paid.

## Rules

- Follow the frozen evaluator lane in `docs/evaluator-lane-lock.json`.
- Start from the official Module Builder minimal universal-module contract.
- Write a failing semantic test before behavior.
- Do not patch official Logos repositories or require evaluator adaptation.
- Keep module implementation Qt-free; generated glue owns the Qt boundary.
- Never commit secrets, wallet material, tokens, personal identifiers, local
  absolute paths, generated caches, or unrelated-project artifacts.
- A nominal load is not proof: require liveness, method discovery, typed call,
  restart, and exact artifact hashes.
- Public release and prize submission require the exact-candidate release gate.

## Verification

Run `python3 -m unittest discover -s tests -v` after contract-layer changes.
Native changes additionally require the pinned Nix build and runtime commands
documented in the spike evidence packet.
