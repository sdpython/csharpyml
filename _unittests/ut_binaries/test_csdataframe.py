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

from src.csharpyml.binaries import CSDataFrame


class TestCsDataFrame(ExtTestCase):
    """Test C# dataframes."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)
        self.assertFalse(datasets is None)

    def test_shape(self):
        data = "AA,BB,CC\n1,4.5,e\n2,-5.6,rr"
        df = CSDataFrame.read_str(data)
        self.assertEqual((df.Shape.Item1, df.Shape.Item2), (2, 3))

    def test_read_str(self):
        data = "AA,BB,CC\n1,4.5,e\n2,-5.6,rr"
        df = CSDataFrame.read_str(data)
        ts = df.ToString()
        self.assertEqual(data, ts)

    def test_read_csv(self):
        data = "AA,BB,CC\n1,4.5,e\n2,-5.6,rr"
        temp = get_temp_folder(self.test_read_csv)
        name = os.path.join(temp, "data.csv")
        with open(name, 'w') as f:
            f.write(data)
        df = CSDataFrame.read_csv(name)
        ts = df.ToString()
        self.assertEqual(data, ts)

    def test_df(self):
        df = pandas.DataFrame(
            data=dict(AA0=[1, 2], AA=[1, 4], BB=[4.5, -5.6], CC=['e', 'rr']))
        df['AA0'] = df['AA0'].astype(numpy.int32)
        csdf = CSDataFrame.read_df(df)
        sch = csdf.Schema
        sch = [csdf.Schema.GetColumnType(i).ToString()
               for i in range(df.shape[1])]
        self.assertEqual(sch, ['I4', 'I8', 'R8', 'Text'])
        df2 = csdf.to_df()
        self.assertEqualDataFrame(df, df2)

    def test_head(self):
        df = pandas.DataFrame(
            data=dict(AA0=[1, 2], AA=[1, 4], BB=[4.5, -5.6], CC=['e', 'rr']))
        df['AA0'] = df['AA0'].astype(numpy.int32)
        csdf = CSDataFrame.read_df(df)
        df1 = csdf.to_df().head(1)
        head = csdf.Head(1)
        df2 = head.to_df()
        self.assertEqual(df1.shape, (1, 4))
        self.assertEqual(df2.shape, (1, 4))
        self.assertEqualDataFrame(df1, df2)


if __name__ == "__main__":
    unittest.main()
