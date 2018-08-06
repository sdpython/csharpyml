"""
@brief      test log(time=3s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
import numpy
from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas
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

from src.csharpyml.binaries import CSPipeline


class TestCsPipeline(ExtTestCase):
    """Test C# Pipeline."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)
        self.assertFalse(datasets is None)

    def test_iris(self):
        X, y = datasets.load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X.astype(numpy.float32), y.astype(numpy.float32))
        assert X_test is not None
        assert y_test is not None
        df = pandas.DataFrame(data=X_train, columns=["FA", "FB", "FC", "FD"])
        df["Label"] = y_train
        pipe = CSPipeline(["concat{col=Feat:FA,FB,FC,FD}"], "lr")
        pipe.fit(df, feature="Feat", label="Label")


if __name__ == "__main__":
    unittest.main()
