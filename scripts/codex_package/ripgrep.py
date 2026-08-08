"""Fetch ripgrep from the DotSlash manifest used by the package builder."""

import platform
import shutil
from pathlib import Path

from .dotslash import fetch_dotslash_executable
from .targets import REPO_ROOT
from .targets import TargetSpec
from .targets import resolve_input_path


RG_MANIFEST = REPO_ROOT / "scripts" / "codex_package" / "rg"


def resolve_rg_bin(spec: TargetSpec, rg_bin: Path | None) -> Path:
    if rg_bin is not None:
        return resolve_input_path(rg_bin, "ripgrep executable", "--rg-bin")

    # ripgrep does not publish a riscv64 Linux archive. Native riscv64 builds
    # can use the host installation; cross-built release packages pass an
    # explicit source-built musl binary with --rg-bin.
    if spec.target.startswith("riscv64gc-") and platform.machine() == "riscv64":
        host_rg = shutil.which("rg")
        if host_rg is not None:
            return Path(host_rg).resolve()

    return fetch_rg(spec)


def fetch_rg(
    spec: TargetSpec,
    *,
    manifest_path: Path = RG_MANIFEST,
) -> Path:
    rg_bin = fetch_dotslash_executable(
        spec,
        manifest_path=manifest_path,
        artifact_label="ripgrep",
        cache_key=f"{spec.target}-rg",
        dest_name=spec.rg_name,
    )
    if rg_bin is None:
        raise AssertionError("ripgrep is required for all package targets")
    return rg_bin
