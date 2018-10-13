"""
@file
@brief Makes :epkg:`C# ScikitPipeline` available in :epkg:`Python`.
"""
import os
import numpy
import pandas
from .add_reference import add_csharpml_extension
from .cs_dataframe import CSDataFrame
from .cs_logging import CSLogging


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
        from CSharPyMLExtension import PyPipelineHelper
        return PyPipelineHelper

    def __init__(self, transforms=None, predictor=None, stdout="store", **kwargs):
        """
        Creates a pipeline :epkg:`C# Pipeline`.

        @param      transforms      list of transforms (can be None)
        @param      predictor       predictor (can be None)
        @param      stdout          see @see cl CSLogging, by default, the class
                                    catches the standard output
        @param      kwargs          see @see cl CSLogging

        The list of available transforms can be obtained by running
        @see fn get_transforms_list, the list of available learners
        can be obtained by running @see fn get_learners_list,
        the command line for each of them is built from the alias
        and the available parameters given by function
        @see fn get_help.

        Example:

        * ``concat{col=Feat:Size,Length}``: adds a transform which concatenates
          two single float columns *Size*, *Length* into one vector column
          named *Feat*.
        * ``ova{p=lr{maxiter=10}}``: defines a learner which applies strategy
          one versus all with a logistic regression, each of them trained
          with at most 10 iterations.
        """
        if transforms is None and predictor is None:
            # Used by read method.
            pass
        else:
            PipelineHelper = CSPipeline.get_cs_class()
            cs_log = CSLogging(stdout=stdout, **kwargs)
            self._cs_log = cs_log
            self._obj = PipelineHelper.CreateScikitPipeline(
                transforms, predictor, cs_log._obj)

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
        elif isinstance(data, numpy.ndarray):
            if len(data.shape) != 2:
                raise ValueError("data must be a matrix.")
            data = CSDataFrame.read_df(data)

        if isinstance(data, CSDataFrame):
            # CSDataFrame
            self._obj.Train(data._obj, feature, label, weight, group_id)
        else:
            # IDataView
            self._obj.Train(data, feature, label, weight, group_id)

    def predict(self, data):
        """
        Predicts with a trained pipeline.

        @param      data        dataframe (*pandas* or *C#*)
        @return                 prediction, with the same type as the one used for data
        """
        return self._predict_transform(data, lambda arg: self._obj.Predict(arg))

    def transform(self, data):
        """
        Transforms with a trained pipeline.

        @param      data        dataframe (*pandas* or *C#*)
        @return                 prediction, with the same type as the one used for data
        """
        return self._predict_transform(data, lambda arg: self._obj.Transform(arg))

    def _predict_transform(self, data, fct):
        """
        Transforms pr predicts with a trained pipeline, there is no predictor.

        @param      data        dataframe (*pandas* or *C#*)
        @return                 prediction, with the same type as the one used for data
        """
        if isinstance(data, pandas.DataFrame):
            data = CSDataFrame.read_df(data)
            convert_back = True
        elif isinstance(data, numpy.ndarray):
            if len(data.shape) != 2:
                raise ValueError("data must be a matrix.")
            data = CSDataFrame.read_df(data)
            convert_back = True
        else:
            convert_back = False

        if isinstance(data, CSDataFrame):
            # CSDataFrame
            res = fct(data._obj)
            dfcs = CSDataFrame.read_view(res)
            if convert_back:
                return dfcs.to_df()
            else:
                return dfcs
        else:
            # IDataView
            return fct(data)

    def save(self, filename):
        """
        Saves the pipeline as a filename.

        @param  filename    filename (zip)
        """
        ext = os.path.splitext(filename)[-1]
        if ext != ".zip":
            raise ValueError("The filename must have extension .zip")
        self._obj.Save(filename)

    @staticmethod
    def load(filename, **kwargs):
        """
        Loads a pipeline from a filename.

        @param  filename    filename (zip)
        @param  kwargs      see @see cl CSLogging
        @return             returns a @see cl CSPipeline
        """
        PipelineHelper = CSPipeline.get_cs_class()
        cs_log = CSLogging(**kwargs)
        PipelineHelper = CSPipeline.get_cs_class()
        obj = PipelineHelper.CreateScikitPipeline(filename, cs_log._obj)
        pipe = CSPipeline()
        pipe._obj = obj
        return pipe

    @property
    def StdOut(self):
        """
        Returns stored stdout.
        """
        return self._cs_log.StdOut

    @property
    def StdErr(self):
        """
        Returns stored stderr.
        """
        return self._cs_log.StdErr
