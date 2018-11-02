"""
@file
@brief Makes :epkg:`C# DataFrame` available in :epkg:`Python`.
"""
from .add_reference import add_csharpml_extension
from .cs_dataframe import CSDataFrame


class CSStreamingDataFrame:
    """
    Wraps :epkg:`C# Streaming DataFrame`.
    """

    @staticmethod
    def get_cs_class():
        """
        Returns the :epkg:`C#` class used to interact
        with :epkg:`C# Streaming DataFrame`.
        """
        add_csharpml_extension()
        from CSharPyMLExtension import PyDataFrameHelper
        return PyDataFrameHelper

    def __init__(self, obj=None):
        """
        Creates an empty :epkg:`C# Streaming DataFrame`.

        @param      obj     :epkg:`C# DataFrame` or None to create an empty one
        """
        if obj is None:
            self._obj = CSStreamingDataFrame.get_cs_class().CreateEmptyDataFrame()
        else:
            self._obj = obj

    @staticmethod
    def read_view(idataview, nrows=-1):
        """
        Converts a :epkg:`C# IDataView` into :epkg:`C# Streaming IDataView`.

        @param      idataview   :epkg:`C# IDataView`
        @param      nrows       keeps only the first rows or -1 for all
        @return                 @see cl CSDataFrame
        """
        cl = CSStreamingDataFrame.get_cs_class()
        obj = cl.ReadStreamingView(idataview, nrows)
        return CSStreamingDataFrame(obj)

    @staticmethod
    def read_csv(filename, sep=',', header=True, names=None,
                 kinds=None, nrows=-1, guess_rows=10, encoding=None,
                 index=False):
        """
        Creates a streaming dataframe from a :epkg:`csv` file.

        @param      filename        filename or list of filenames
        @param      sep             separator
        @param      header          has header
        @param      names           columns names (if no header)
        @param      kinds           types of each columns (see below)
        @param      nrows           keeps only the first rows or -1 for all
        @param      guess_rows      number of rows to guess the type is not overriden by
                                    kinds
        @param      encoding        encoding
        @param      index           add a column with the row index
        @return                     @see cl CSDataFrame

        *kinds* can be None to let the function guess the right type,
        or it can be an array to change the type of every column.
        *-1* indicates the function should guess.
        """
        cl = CSStreamingDataFrame.get_cs_class()
        if isinstance(filename, list):
            obj = cl.ReadStreamingCsvs(
                filename, sep, header, names, kinds, nrows, guess_rows, encoding, index)
        else:
            obj = cl.ReadStreamingCsv(
                filename, sep, header, names, kinds, nrows, guess_rows, encoding, index)
        return CSStreamingDataFrame(obj)

    def to_csdf(self):
        """
        Converts into :epkg:`C# DataFrame`.
        """
        return CSDataFrame(self._obj.ToDataFrame())
