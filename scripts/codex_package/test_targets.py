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


if __name__ == "__main__":
    unittest.main()
