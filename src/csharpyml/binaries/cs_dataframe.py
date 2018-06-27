"""
@file
@brief Makes C# Dataframe available in Python.
"""
from collections import OrderedDict
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
        for i in range(df.shape[1]):
            col = list(df.iloc[:, i])
            print(i, type(col), col)
            cl.AddColumnToDataFrame(res._obj, names[i], col)
        return res
        
    @staticmethod
    def read_csv(filename, sep=',', header=True, names=None,
                 kinds=None, nrows=-1, guess_rows=10):
        """
        Creates a dataframe from a :epkg:`csv` file.
        
        @param      filename        filename
        @param      sep             separator
        @param      header          has header
        @param      names           columns names (if no header)
        @param      kinds           types of each columns (see below)
        @param      guess_rows      number of rows to guess the type is not overriden by
                                    kinds
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
        return CSDataFrame(CSDataFrame.get_cs_class().ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows))
        
    @staticmethod
    def read_str(content, sep=',', header=True, names=None,
                 kinds=None, nrows=-1, guess_rows=10):
        """
        Creates a dataframe from a string.
        
        @param      content         string
        @param      sep             separator
        @param      header          has header
        @param      names           columns names (if no header)
        @param      kinds           types of each columns (see below)
        @param      guess_rows      number of rows to guess the type is not overriden by
                                    kinds
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
        return CSDataFrame(CSDataFrame.get_cs_class().ReadStr(content, sep, header, names, kinds, nrows, guess_rows))
    
    def __str__(self):
        """
        usual
        """
        return CSDataFrame.get_cs_class().DataFrameToString(self._obj)
    
    def to_df(self):
        """
        Converts the :epkg:`C# DataFrame` back into a
        :epkg:`DataFrame`.
        """
        shape = self._obj.Shape
        data = OrderedDict()
        schema = self._obj.Schema
        for i in range(shape[1]):
            name = schema.GetColumnName(i)
            kind = schema.GetColumnType(i)
            print(name, kind)
    
    def __getattr__(self, name):
        """
        Looks first in the Python class then in the :epkg:`C#` class.
        """
        if hasattr(self.__class__, name):
            return getattr(self.__class__, name)
        elif hasattr(self._obj, name):
            return getattr(self._obj, name)
        else:
            raise AttributeError("Class '{0}' has no attribute '{1}'".format(self.__class__.__name__, name))
            
        
