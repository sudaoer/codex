import unittest
from unittest.mock import patch

from .targets import default_target


class DefaultTargetTest(unittest.TestCase):
    def test_riscv64_linux_defaults_to_musl_release_target(self) -> None:
        with (
            patch(
                "scripts.codex_package.targets.platform.system", return_value="Linux"
            ),
            patch(
                "scripts.codex_package.targets.platform.machine",
                return_value="riscv64",
            ),
        ):
            self.assertEqual(default_target(), "riscv64gc-unknown-linux-musl")

    def test_riscv64a23_target_is_explicit(self) -> None:
        from .targets import TARGET_SPECS

        spec = TARGET_SPECS["riscv64a23-unknown-linux-gnu"]
        self.assertTrue(spec.is_linux)
        self.assertEqual(spec.dotslash_platform, "linux-riscv64a23")


if __name__ == "__main__":
    unittest.main()
