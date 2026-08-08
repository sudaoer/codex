# RISC-V 64-bit Linux

Codex supports `riscv64gc-unknown-linux-gnu` for the baseline RISC-V build,
`riscv64gc-unknown-linux-musl` for release packages, and the explicit
RVA23U64 target `riscv64a23-unknown-linux-gnu`. The release workflow
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

For an RVA23U64 build, install Rust's official GNU target and use the same
cross sysroot with the target-specific environment variable names:

```sh
rustup target add riscv64a23-unknown-linux-gnu
export CARGO_TARGET_RISCV64A23_UNKNOWN_LINUX_GNU_LINKER=riscv64-linux-gnu-gcc
export OPENSSL_LIB_DIR=/opt/codex-riscv64-sysroot/usr/lib/riscv64-linux-gnu
export OPENSSL_INCLUDE_DIR=/opt/codex-riscv64-sysroot/usr/include
export CFLAGS_riscv64a23_unknown_linux_gnu=-I/opt/codex-riscv64-sysroot/usr/include/riscv64-linux-gnu
export CARGO_TARGET_RISCV64A23_UNKNOWN_LINUX_GNU_RUSTFLAGS='-C link-arg=-Wl,-rpath-link,/opt/codex-riscv64-sysroot/usr/lib/riscv64-linux-gnu'
cargo build --locked --target riscv64a23-unknown-linux-gnu --bin codex
```

The Rust 1.95.0 toolchain used for the current cross-build also has an
optimized RISC-V code-generation failure in the LLVM loop vectorizer while
building the full `codex` binary. The unoptimized debug binary and the
optimized `codex-code-mode-host` build succeed; use a newer Rust/LLVM toolchain
for an optimized full CLI release if this failure reproduces.

Rust currently provides the official RVA23 target for GNU Linux, not a
`riscv64a23-unknown-linux-musl` target. Keep the musl release on `rv64gc`
until Rust publishes a matching musl target; do not substitute a custom JSON
target in stable release builds.

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

The V8 `rv64gc` build disables Highway's optional RVV runtime-dispatch path so
the baseline binary does not require the V extension. The separate RVA23 V8
pair is compiled with `-march=rva23u64`, which enables the mandatory V/RVV
instructions for that target. These settings affect SIMD acceleration in
Highway users, not V8's RISC-V JIT support.

## Release package contents

The primary RISC-V musl package contains `codex`, `codex-code-mode-host`, a
target-built `bwrap`, and a target-built `rg`. The
`codex-responses-api-proxy` is published as its own static RISC-V artifact.
The patched zsh resource is optional; it is included only after a
`linux-riscv64` artifact is present in the selected zsh DotSlash manifest.
