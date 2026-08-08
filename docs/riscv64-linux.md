# RISC-V 64-bit Linux

Codex supports `riscv64gc-unknown-linux-gnu` for native development and
`riscv64gc-unknown-linux-musl` for release packages. The release workflow
cross-compiles RISC-V artifacts on an x86_64 Linux runner.

## Development build

Install Rust 1.95 with the GNU RISC-V target, a
`riscv64-linux-gnu-gcc` toolchain, and target OpenSSL development files. Then
run from `codex-rs`:

```sh
export CARGO_TARGET_RISCV64GC_UNKNOWN_LINUX_GNU_LINKER=riscv64-linux-gnu-gcc
export OPENSSL_LIB_DIR=/opt/codex-riscv64-sysroot/usr/lib/riscv64-linux-gnu
export OPENSSL_INCLUDE_DIR=/opt/codex-riscv64-sysroot/usr/include
export CFLAGS_riscv64gc_unknown_linux_gnu=-I/opt/codex-riscv64-sysroot/usr/include/riscv64-linux-gnu
export CARGO_TARGET_RISCV64GC_UNKNOWN_LINUX_GNU_RUSTFLAGS='-C link-arg=-Wl,-rpath-link,/opt/codex-riscv64-sysroot/usr/lib/riscv64-linux-gnu'
cargo build --locked --target riscv64gc-unknown-linux-gnu --bin codex
```

The OpenSSL headers and shared libraries in the sysroot must come from the same
target distribution release. A static Bianbu OpenSSL link also needs its
transitive zlib and jitterentropy archives, so the development example uses the
matching shared libraries already present on the target instead.

On a native RISC-V host, the package builder uses an installed `rg` when no
RISC-V entry exists in the ripgrep DotSlash manifest. Release builds compile
ripgrep 15.2.0 with PCRE2 support from source and pass it through `--rg-bin`,
so release packages do not depend on the build host's ripgrep binary.

## Code mode and V8

Code mode uses Codex-built `rusty_v8` artifacts. Before publishing a Codex
release, run the `rusty-v8-release` workflow for both RISC-V GNU and musl
targets and both `release` and `ptrcomp-sandbox` variants. The normal Codex
release consumes the `ptrcomp-sandbox` musl pair.

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
