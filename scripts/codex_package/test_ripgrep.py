import unittest
from unittest.mock import patch

from .ripgrep import resolve_rg_bin
from .targets import TARGET_SPECS


class ResolveRgBinTest(unittest.TestCase):
    def test_riscv64_native_build_uses_system_ripgrep(self) -> None:
        spec = TARGET_SPECS["riscv64gc-unknown-linux-gnu"]

        with (
            patch(
                "scripts.codex_package.ripgrep.platform.machine",
                return_value="riscv64",
            ),
            patch(
                "scripts.codex_package.ripgrep.shutil.which", return_value="/usr/bin/rg"
            ),
        ):
            self.assertEqual(resolve_rg_bin(spec, None).as_posix(), "/usr/bin/rg")


if __name__ == "__main__":
    unittest.main()
