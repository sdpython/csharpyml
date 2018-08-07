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
from pyquickhelper.pycode import ExtTestCase, get_temp_folder

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

    def test_predictor(self):
        X, y = datasets.load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X.astype(numpy.float32), y.astype(numpy.float32))
        df_train = pandas.DataFrame(data=X_train, columns=[
                                    "FA", "FB", "FC", "FD"])
        df_train["Label"] = y_train
        pipe = CSPipeline(["concat{col=Feat:FA,FB,FC,FD}"],
                          "ova{p=lr}", stdout="C#", verbose=0)
        pipe.fit(df_train, feature="Feat", label="Label")
        df_test = pandas.DataFrame(data=X_test, columns=[
                                   "FA", "FB", "FC", "FD"])
        self.assertIsInstance(df_test, pandas.DataFrame)
        df_test["Label"] = y_test
        pred = pipe.predict(df_test)
        head = pred.head()
        exp = ['FA', 'FB', 'FC', 'FD', 'Label', 'Feat.0', 'Feat.1', 'Feat.2',
               'Feat.3', 'PredictedLabel', 'Score.0', 'Score.1', 'Score.2']
        self.assertEqual(list(head.columns), exp)
        self.assertEqual(pred.shape, (38, 13))
        acc = (pred.Label + 1 - pred.PredictedLabel).abs().sum()
        self.assertLesser(acc, 10)
        # Save
        temp = get_temp_folder(__file__, "temp_predictor")
        outfile = os.path.join(temp, "iris.zip")
        pipe.save(outfile)
        pipe2 = CSPipeline.load(outfile)
        pred2 = pipe2.predict(df_test)
        self.assertEqual(pred, pred2)

    def test_transform(self):
        X, y = datasets.load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X.astype(numpy.float32), y.astype(numpy.float32))
        df_train = pandas.DataFrame(data=X_train, columns=[
                                    "FA", "FB", "FC", "FD"])
        df_train["Label"] = y_train
        pipe = CSPipeline(
            ["concat{col=Feat:FA,FB,FC,FD}", "poly{col=Feat}"], stdout="python", verbose=0)
        pipe.fit(df_train)
        df_test = pandas.DataFrame(data=X_test, columns=[
                                   "FA", "FB", "FC", "FD"])
        self.assertIsInstance(df_test, pandas.DataFrame)
        df_test["Label"] = y_test
        pred = pipe.transform(df_test)
        head = pred.head()
        exp = ['FA', 'FB', 'FC', 'FD', 'Label', 'Feat.0', 'Feat.1', 'Feat.2', 'Feat.3', 'Feat.4',
               'Feat.5', 'Feat.6', 'Feat.7', 'Feat.8', 'Feat.9', 'Feat.10', 'Feat.11', 'Feat.12', 'Feat.13']
        self.assertEqual(list(head.columns), exp)
        self.assertEqual(pred.shape, (38, 19))
        # Save
        temp = get_temp_folder(__file__, "temp_transform")
        outfile = os.path.join(temp, "iris_poly.zip")
        pipe.save(outfile)
        pipe2 = CSPipeline.load(outfile)
        pred2 = pipe2.predict(df_test)
        self.assertEqual(pred, pred2)

    def test_transform_array(self):
        X, y = datasets.load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X.astype(numpy.float32), y.astype(numpy.float32))
        pipe = CSPipeline(
            ["concat{col=Feat:X0,X1,X2,X3}", "poly{col=Feat}"], stdout="python", verbose=0)
        pipe.fit(X_train)
        pred = pipe.transform(X_test)
        head = pred.head()
        exp = ['X0', 'X1', 'X2', 'X3', 'Feat.0', 'Feat.1', 'Feat.2', 'Feat.3', 'Feat.4',
               'Feat.5', 'Feat.6', 'Feat.7', 'Feat.8', 'Feat.9', 'Feat.10', 'Feat.11', 'Feat.12', 'Feat.13']
        self.assertEqual(list(head.columns), exp)
        self.assertEqual(pred.shape, (38, 18))
        # Save
        temp = get_temp_folder(__file__, "temp_transform_array")
        outfile = os.path.join(temp, "iris_poly.zip")
        pipe.save(outfile)
        pipe2 = CSPipeline.load(outfile)
        pred2 = pipe2.predict(X_test)
        self.assertEqual(pred, pred2)


if __name__ == "__main__":
    unittest.main()
