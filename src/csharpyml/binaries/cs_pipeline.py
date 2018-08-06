"""
@file
@brief Makes :epkg:`C# ScikitPipeline` available in :epkg:`Python`.
"""
import pandas
from .add_reference import add_csharpml_extension
from .cs_dataframe import CSDataFrame


class CSPipeline:
    """
    Wraps :epkg:`C# ScikitPipeline`.
    """

    @staticmethod
    def get_cs_class():
        """
        Returns the :epkg:`C#` class used to interact
        with :epkg:`C# Pipeline`.
        """
        add_csharpml_extension()
        from CSharPyMLExtension import PipelineHelper
        return PipelineHelper

    def __init__(self, transforms=None, predictor=None):
        """
        Creates a pipeline :epkg:`C# Pipeline`.

        @param      transforms      list of transforms (can be None)
        @param      predictor       predictor (can be None)
        """
        PipelineHelper = CSPipeline.get_cs_class()
        self._obj = PipelineHelper.CreateScikitPipeline(transforms, predictor)

    def fit(self, data, feature=None, label=None, group_id=None, weight=None):
        """
        Fits a pipeline.

        @param      data        dataframe (*pandas* or *C#*)
        @param      feature     if a predictor is specified,
                                specifiy which column to use as features
        @param      label       if a supervized predictor is specified,
                                specifiy which column to use as label
        @param      weight      if a predictor is specified,
                                specifiy which column to use as weight
        @param      group_id    if a ranker is specified,
                                specifiy which column to use as features
        @return                 self
        """
        if isinstance(data, pandas.DataFrame):
            data = CSDataFrame.read_df(data)
        self._obj.Train(data._obj, feature, label, weight, group_id)
