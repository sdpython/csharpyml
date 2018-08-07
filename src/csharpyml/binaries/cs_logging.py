"""
@file
@brief Makes :epkg:`C# ScikitPipeline` available in :epkg:`Python`.
"""
import sys
import pandas
from .add_reference import add_csharpml_extension
from .cs_dataframe import CSDataFrame


class CSLogging:
    """
    Wraps :epkg:`C# LogWriter`.
    """

    @staticmethod
    def get_cs_class():
        """
        Returns the :epkg:`C#` class used to interact
        with :epkg:`C# Pipeline`.
        """
        add_csharpml_extension()
        from CSharPyMLExtension import EnvHelper
        return EnvHelper

    @staticmethod
    def print_stdout(text):
        sys.stdout.write(text.strip("\r"))

    @staticmethod
    def print_stderr(text):
        sys.stderr.write(text.strip("\r"))

    def __init__(self, stdout="python", seed=-1, verbose=True, sensitivity="All", conc=0):
        """
        Creates en environment which defines multiple variables such
        as the random seed, more or less display, the sensitivity of message,
        the type of output.

        @param      stdout          ``'python'`` or ``'C#'``, where the log should
                                    be printed, on the standard python output or the C#'s one.
                                    The *C#* output is faster but appears on Jupyter's servee
                                    standard output instead of the notebook itself.
        @param      seed            seed for random generator, -1 for a random one
        @param      verbose         display training information or not
        @param      sensitivity     *All*, *None*, *UserData*, *Schema*, defines what kind of
                                    information to display on the standard output and in the
                                    error messages
        @param      conc            number of threads to use while training, 0 to get
                                    a number of threads depending on the processor,
                                    it is usually better to use the C# output for a better speed
                                    and avoid GIL lock.

        """
        EnvHelper = CSLogging.get_cs_class()

        if stdout == "C#":
            self._obj = EnvHelper.CreateConsoleEnvironment(
                seed, verbose, sensitivity, conc)
        elif stdout == "python":
            del_out = EnvHelper.PrintDelegate(CSLogging.print_stdout)
            del_err = EnvHelper.PrintDelegate(CSLogging.print_stderr)
            self._obj = EnvHelper.CreatePythonEnvironment(seed, verbose, sensitivity, conc,
                                                          del_out, del_err)
        else:
            raise ValueError(
                "Unable to interpret parameter stdout='{0}'".format(stdout))
