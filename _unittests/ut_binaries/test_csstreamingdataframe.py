"""
@brief      test log(time=3s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
from sklearn import datasets
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

from src.csharpyml.binaries import CSStreamingDataFrame


class TestCsStreamingDataFrame(ExtTestCase):
    """Test C# dataframes."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)
        self.assertFalse(datasets is None)

    def test_read_csv(self):
        data = "AA,BB,CC\n1,4.5,e\n2,-5.6,rr"
        temp = get_temp_folder(self.test_read_csv)
        name = os.path.join(temp, "data.csv")
        with open(name, 'w') as f:
            f.write(data)
        sdf = CSStreamingDataFrame.read_csv(name)
        df = sdf.to_csdf()
        ts = df.ToString()
        self.assertEqual(data, ts)


if __name__ == "__main__":
    unittest.main()
