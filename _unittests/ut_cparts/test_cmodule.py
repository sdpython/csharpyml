"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.csharpy.cparts import version_c


class TestCModule(ExtTestCase):
    """Test dynamic compilation."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_version_c(self):
        ver = version_c()
        self.assertEqual(ver, "0.1")


if __name__ == "__main__":
    unittest.main()
