"""
@brief      test log(time=3s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
from sklearn import datasets
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

from src.csharpyml.binaries import get_mlnet_assemblies


class TestCsCommonDependencies(ExtTestCase):
    """Test C# dataframes."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)
        self.assertFalse(datasets is None)

    def test_common_dependencies(self):
        deps, using = get_mlnet_assemblies()
        self.assertNotEmpty(deps)
        self.assertNotEmpty(using)


if __name__ == "__main__":
    unittest.main()
