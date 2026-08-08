# RISC-V 64-bit Linux

Codex supports `riscv64gc-unknown-linux-musl` for release packages. The
release workflow cross-compiles RISC-V artifacts on an x86_64 Linux runner.

## Code mode and V8

Code mode uses Codex-built `rusty_v8` artifacts. Before publishing a Codex
release, run the `rusty-v8-release` workflow for the RISC-V musl target and
both `release` and `ptrcomp-sandbox` variants. The normal Codex release
consumes the `ptrcomp-sandbox` musl pair.

V8 requests a 128 GiB sandbox reservation on RISC-V. A Sv39 kernel cannot
reserve the full ideal address space, so V8 falls back to a partially reserved
sandbox. Code mode remains enabled, but its address-space isolation is weaker
than on a host that can reserve the complete V8 sandbox. This is an accepted
platform limitation, not a silent change to the code-mode feature set.

The V8 build disables Highway's optional RVV runtime-dispatch path so the
published binary keeps the Rust target's `rv64gc` baseline and does not require
the V extension. This affects SIMD acceleration in Highway users, not V8's
RISC-V JIT support.

## Release package contents

The primary RISC-V musl package contains `codex`, `codex-code-mode-host`, a
target-built `bwrap`, and a target-built `rg`. The
`codex-responses-api-proxy` is published as its own static RISC-V artifact.
The patched zsh resource is optional; it is included only after a
`linux-riscv64` artifact is present in the selected zsh DotSlash manifest.
