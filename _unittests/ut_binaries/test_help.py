"""
@brief      test log(time=3s)

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

from src.csharpyml.binaries import get_transforms_list, get_learners_list, get_help


class TestHelp(ExtTestCase):
    """Test maml command line."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_transforms(self):
        tr = get_transforms_list()
        self.assertIn("CategoricalTransform", tr)
        self.assertIn("NearNeighborsTransform", tr)

    def test_learners(self):
        tr = get_learners_list()
        self.assertIn("LogisticRegression", tr)
        self.assertIn("NearestNeighborsBC", tr)

    def test_help(self):
        tr = get_help("lr")
        self.assertIn("LogisticRegression", tr)
        self.assertIn("maxIterations=<int> ", tr)


if __name__ == "__main__":
    unittest.main()
