import unittest

from scripts.validate_stable_diff import validate


class StableDiffTests(unittest.TestCase):
    def test_stable_promotion_matches_allowed_diff(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
