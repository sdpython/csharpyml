"""
@file
@brief Makes C# Dataframe available in Python.
"""
from collections import OrderedDict
import numpy
import pandas
from .add_reference import add_csharpml_extension


class CSDataFrame:
    """
    Wraps :epkg:`C# DataFrame`.
    """

    @staticmethod
    def get_cs_class():
        """
        Returns the :epkg:`C#` class used to interact
        with :epkg:`C# DataFrame`.
        """
        add_csharpml_extension()
        from CSharPyMLExtension import DataFrameHelper
        return DataFrameHelper

    def __init__(self, obj=None):
        """
        Creates an empty :epkg:`C# DataFrame`.

        @param      obj     :epkg:`C# DataFrame` or None to create an empty one
        """
        if obj is None:
            self._obj = CSDataFrame.get_cs_class().CreateEmptyDataFrame()
        else:
            self._obj = obj

    @staticmethod
    def read_df(df):
        """
        Converts a :epkg:`DataFrame` into a :epkg:`C# DataFrame`.

        @param      df      :epkg:`DataFrame`
        @return             @see cl CSDataFrame
        """
        cl = CSDataFrame.get_cs_class()
        res = CSDataFrame()
        names = df.columns
        dtypes = df.dtypes
        for i in range(df.shape[1]):
            col = list(df.iloc[:, i])
            typ = dtypes[i]
            if typ == numpy.bool_:
                cl.AddColumnToDataFramebool(res._obj, names[i], col)
            elif typ == numpy.uint32:
                cl.AddColumnToDataFrameuint(res._obj, names[i], col)
            elif typ == numpy.int32:
                cl.AddColumnToDataFrameint32(res._obj, names[i], col)
            elif typ == numpy.int64:
                cl.AddColumnToDataFrameint64(res._obj, names[i], col)
            elif typ == numpy.float32:
                cl.AddColumnToDataFramefloat32(res._obj, names[i], col)
            elif typ == numpy.float64:
                cl.AddColumnToDataFramefloat64(res._obj, names[i], col)
            else:
                cl.AddColumnToDataFramestring(res._obj, names[i], col)
        return res

    @staticmethod
    def read_csv(filename, sep=',', header=True, names=None,
                 kinds=None, nrows=-1, guess_rows=10, encoding=None,
                 index=False):
        """
        Creates a dataframe from a :epkg:`csv` file.

        @param      filename        filename
        @param      sep             separator
        @param      header          has header
        @param      names           columns names (if no header)
        @param      kinds           types of each columns (see below)
        @param      guess_rows      number of rows to guess the type is not overriden by
                                    kinds
        @param      encoding        encoding
        @param      index           add a column with the row index
        @return                     @see cl CSDataFrame

        *kinds* can be None to let the function guess the right type,
        or it can be an array to change the type of every column.
        *-1* indicates the function should guess.

        .. faqref::
            :title: What are kinds?

            *kind* are an enum class which indicates the type
            of a variable or an array. It is equivalent to an integer.
            The mapping is defined in file :epkg:`DataKind`.
        """
        return CSDataFrame(CSDataFrame.get_cs_class().ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows, encoding, index))

    @staticmethod
    def read_str(content, sep=',', header=True, names=None,
                 kinds=None, nrows=-1, guess_rows=10, index=False):
        """
        Creates a dataframe from a string.

        @param      content         string
        @param      sep             separator
        @param      header          has header
        @param      names           columns names (if no header)
        @param      kinds           types of each columns (see below)
        @param      guess_rows      number of rows to guess the type is not overriden by
                                    kinds
        @param      index           add a column with the row index
        @return                     @see cl CSDataFrame

        *kinds* can be None to let the function guess the right type,
        or it can be an array to change the type of every column.
        *-1* indicates the function should guess.

        .. faqref::
            :title: What are kinds?

            *kind* are an enum class which indicates the type
            of a variable or an array. It is equivalent to an integer.
            The mapping is defined in file :epkg:`DataKind`.
        """
        return CSDataFrame(CSDataFrame.get_cs_class().ReadStr(content, sep, header, names, kinds, nrows, guess_rows, index))

    def __str__(self):
        """
        usual
        """
        return CSDataFrame.get_cs_class().DataFrameToString(self._obj)

    def to_df(self):
        """
        Converts the :epkg:`C# DataFrame` back into a
        :epkg:`DataFrame`.

        .. todo::
            This function does too many copies.
            It should allocated arrays and ask
            the C# code to copy the data in it.
        """
        # DataKind
        # I1 = 1, U1 = 2, I2 = 3, U2 = 4, I4 = 5, U4 = 6, I8 = 7, U8 = 8,
        # R4 = 9, Num = 9, R8 = 10, TX = 11, TXT = 11, Text = 11, BL = 12, Bool = 12,
        # TS = 13, TimeSpan = 13, DT = 14, DateTime = 14, DZ = 15, DateTimeZone = 15,
        # UG = 16, U16 = 16
        cl = CSDataFrame.get_cs_class()
        if self._obj.Source is None:
            obj = self._obj
        else:
            obj = self._obj.Copy()

        shape = self._obj.Shape
        data = OrderedDict()
        schema = self._obj.Schema
        apply = []
        for i in range(shape.Item2):
            name = schema.GetColumnName(i)
            kind = schema.GetColumnType(i).ToString()
            if kind == 'I4':
                data[name] = list(
                    cl.DataFrameColumnToArrrayint32(obj, i))
                apply.append((name, numpy.int32))
            elif kind == 'U4':
                data[name] = list(cl.DataFrameColumnToArrrayuint(obj, i))
            elif kind == 'I8':
                data[name] = list(
                    cl.DataFrameColumnToArrrayint64(obj, i))
            elif kind == 'R4':
                data[name] = list(
                    cl.DataFrameColumnToArrrayfloat32(obj, i))
                apply.append((name, numpy.float32))
            elif kind == 'R8':
                data[name] = list(
                    cl.DataFrameColumnToArrrayfloat64(obj, i))
            elif kind in {'TX', 'Text'}:
                data[name] = list(
                    cl.DataFrameColumnToArrraystring(obj, i))
            elif kind in {'BL', 'Bool'}:
                data[name] = list(cl.DataFrameColumnToArrraybool(obj, i))
            else:
                raise TypeError(
                    "Unable to handle type kind {0} for column {1}: '{2}'.".format(kind, i, name))
        res = pandas.DataFrame(data)
        for name, ty in apply:
            res[name] = res[name].astype(ty)
        return res

    class _wrap_return_:
        """
        Wraps a C# object into a Python
        if the returned object is a DataFrame.
        """

        def __init__(self, name, fct):
            self.name = name
            self.fct = fct

        def __call__(self, *args, **kwargs):
            ret = self.fct(*args, **kwargs)
            if hasattr(ret, "GroupBy"):
                return CSDataFrame(ret)
            else:
                return ret

    def __getattr__(self, name):
        """
        Looks first in the Python class then in the :epkg:`C#` class.
        """
        if hasattr(self.__class__, name):
            # Python
            return getattr(self.__class__, name)
        elif hasattr(self._obj, name):
            # C#, wrapped results.
            if name in {'Shape', 'Schema', 'Length', 'Columns', 'ColumnCount',
                        'ALL', 'Kinds', 'Source', 'ColumnsSet', 'loc', 'iloc',
                        'CanShuffle'}:
                # Property
                return getattr(self._obj, name)
            else:
                return CSDataFrame._wrap_return_(name, getattr(self._obj, name))
        else:
            raise AttributeError("Class '{0}' has no attribute '{1}'".format(
                self.__class__.__name__, name))
