"""
@file
@brief Implements function around :epkg:`ML.net` command line.
"""
from .add_reference import AddReference, add_csharpml_extension


def maml(script, catch_output=True, conc=0, verbose=2, sensitivity=-1):
    """
    Runs a *maml script* through :epkg:`ML.net`.
    @param      script          script
    @param      catch_output    the function returns the output as a result at of the
                                execution, otherwise, it gets printed on stdout
                                while being executed
    @param      conc            concurrency (number of threads or 0 to let the library choose)
    @param      verbose         more or less display
    @param      sensitivity     to hide information about data
    @return                     stdout, stderr

    See notebook :ref:`csharpformlinnotebookrst`
    for an example.
    """
    add_csharpml_extension()
    from CSharPyMLExtension import PyMamlHelper
    if catch_output:
        res = PyMamlHelper.MamlScript(
            script, True, conc, verbose, sensitivity, True)
        res = res.replace('\r', '')
        if '--ERR--' in res:
            out, err = res.split('--ERR--')
        else:
            out, err = res, ""
        if '--OUT--' in res:
            out = out.split('--OUT--')[-1]
        return out.strip(' \n\r'), err.strip(' \n\r')
    else:
        PyMamlHelper.MamlScript(script, False, conc,
                                verbose, sensitivity, True)
        return None, None


def get_maml_helper():
    """
    Returns the :epkg:`MamlHelper`.
    """
    add_csharpml_extension()
    AddReference('Scikit.ML.DocHelperMlExt')
    from Scikit.ML.DocHelperMlExt import MamlHelper  # pylint: disable=E0401
    return MamlHelper


def get_transforms_list():
    """
    Returns the list of transforms as a unique strings
    to display.

    .. runpython::
        :showcode:

        from csharpyml.binaries import get_transforms_list
        print(get_transforms_list())
    """
    out, _ = maml("? kind=datatransform")
    return out


def get_learners_list():
    """
    Returns the list of learners as a unique strings
    to display.

    .. runpython::
        :showcode:

        from csharpyml.binaries import get_learners_list
        print(get_learners_list())
    """
    out, _ = maml("? kind=trainer")
    return out


def get_help(cl):
    """
    Returns short documentation on one transform or learner.

    @param      cl      transform or learner name
    @return             string

    .. runpython::
        :showcode:

        from csharpyml.binaries import get_help
        print(get_help("lr"))
    """
    out, _ = maml("? " + cl)
    return out
