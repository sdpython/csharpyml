"""
@brief      test log(time=6s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
from sklearn import datasets
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

from src.csharpyml.binaries import maml


class TestMaml(ExtTestCase):
    """Test maml command line."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_maml(self):
        temp = get_temp_folder(__file__, "temp_maml")

        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        df = pandas.DataFrame(
            X, columns=['Slength', 'Swidth', 'Plength', 'Pwidth'])
        df["Label"] = y
        df = df[["Label"] + ['Slength', 'Swidth', 'Plength', 'Pwidth']]
        dest = os.path.join(temp, "iris_data_id.txt")
        df.to_csv(dest, sep=',', index=False)
        model = os.path.join(temp, "model.zip")

        script = """
        train
        data=__DATA__
        loader=text{col=Label:U4[0-2]:0 col=Slength:R4:1 col=Swidth:R4:2 col=Plength:R4:3 col=Pwidth:R4:4 sep=, header=+}
        xf=Concat{col=Features:Slength,Swidth}
        tr=ova{p=lr}
        out=__MODEL__
        """.strip("\n ").replace('__MODEL__', model).replace('__DATA__', dest)

        out, _ = maml(script, catch_output=False)
        self.assertExists(model)
        self.assertIn("LBFGS Optimizer", out)


if __name__ == "__main__":
    unittest.main()
