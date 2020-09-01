import unittest

from sparkle.version import SparkleVersion

class TestSparkleVersion(unittest.TestCase):
    def test_version_parts(self):
        test_cases = [
            ('1', ['1']),
            ('0.1', ['0', '1']),
            ('0.1-beta', ['0', '1']),
            ('0,1', ['0', '1']),
            ('a.b', ['a', 'b']),
        ]
        for version, expected_parts in test_cases:
            self.assertEqual(SparkleVersion(version).version_parts(), expected_parts)

    def test_sorting_by_version(self):
        test_cases = [
            (['2', '1'], ['1', '2']),
            (['1.10', '1.2'], ['1.2', '1.10']),
            (['1.1.1', '1.1'], ['1.1', '1.1.1']),
            (['1', 'a'], ['a', '1']),
        ]
        for versions, expected in test_cases:
            sv = [SparkleVersion(v) for v in versions]
            sv = sorted(sv)
            sv = [v.version_string for v in sv]
            self.assertEqual(sv, expected)

if __name__ == "__main__":
    unittest.main()
