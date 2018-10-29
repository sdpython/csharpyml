"""
@file
@brief Makes :epkg:`C# ScikitPipeline` available in :epkg:`Python`.
"""
import sys
from io import StringIO
from .add_reference import add_csharpml_extension


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
        from CSharPyMLExtension import PyEnvHelper
        return PyEnvHelper

    @staticmethod
    def print_stdout(text):
        "Writes on ``sys.stdout``."
        sys.stdout.write(text.strip("\r"))

    @staticmethod
    def print_stderr(text):
        "Writes on ``sys.stderr``."
        sys.stderr.write(text.strip("\r"))

    @staticmethod
    def print_stderr_out(text):
        "Writes on ``sys.stdout``."
        sys.stdout.write(text.strip("\r"))

    def __init__(self, stdout="python", seed=-1, verbose=0, sensitivity="All", conc=0):
        """
        Creates en environment which defines multiple variables such
        as the random seed, more or less display, the sensitivity of message,
        the type of output.

        @param      stdout          ``'python'`` or ``'C#'``, where the log should
                                    be printed, on the standard python output or the C#'s one.
                                    The *C#* output is faster but appears on Jupyter's server
                                    standard output instead of the notebook itself.
                                    A third option is available, ``'notebook'`` to let C#
                                    catch the standard output and retrieve it later.
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
        elif stdout == "store":
            del_out = EnvHelper.PrintDelegate(self.logout)
            del_err = EnvHelper.PrintDelegate(self.logerr)
            self._stdout = StringIO()
            self._stderr = StringIO()
            self._obj = EnvHelper.CreatePythonEnvironment(seed, verbose, sensitivity, conc,
                                                          del_out, del_err)
        elif stdout == "python":
            del_out = EnvHelper.PrintDelegate(CSLogging.print_stdout)
            del_err = EnvHelper.PrintDelegate(CSLogging.print_stderr)
            self._obj = EnvHelper.CreatePythonEnvironment(seed, verbose, sensitivity, conc,
                                                          del_out, del_err)
        elif stdout == "python2":
            del_out = EnvHelper.PrintDelegate(CSLogging.print_stdout)
            del_err = EnvHelper.PrintDelegate(CSLogging.print_stderr_out)
            self._obj = EnvHelper.CreatePythonEnvironment(seed, verbose, sensitivity, conc,
                                                          del_out, del_err)
        elif stdout == "notebook":
            obj = EnvHelper.CreateStoreEnvironment(
                seed, verbose, sensitivity, conc)
            self._obj = obj.Item1
            self._csstdout = obj.Item2
            self._csstderr = obj.Item3
        else:
            raise ValueError(
                "Unable to interpret parameter stdout='{0}'".format(stdout))

    def logout(self, text):
        """
        Stores stdout.
        """
        self._stdout.write(text)

    def logerr(self, text):
        """
        Stores stderr.
        """
        self._stderr.write(text)

    @property
    def StdOut(self):
        """
        Returns stored stdout.
        """
        if hasattr(self, "_csstdout"):
            return self._csstdout.ToString()
        elif hasattr(self, "_stdout"):
            return self._stdout.getvalue()
        else:
            raise RuntimeError(
                "Output was not saved. Use stdout='python' or 'notebook'.")

    @property
    def StdErr(self):
        """
        Returns stored stderr.
        """
        if hasattr(self, "_csstderr"):
            return self._csstderr.ToString()
        elif hasattr(self, "_stderr"):
            return self._stderr.getvalue()
        else:
            raise RuntimeError(
                "Output was not saved. Use stdout='python' or 'notebook'.")
