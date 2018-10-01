"""
@file
@brief Implements function around :epkg:`ML.net` command line.
"""
from .add_reference import AddReference


def maml(script, catch_output=True):
    """
    Runs a *maml script* through :epkg:`ML.net`.
    @param      script          script
    @param      catch_output    the function returns the output as a result at of the
                                execution, otherwise, it gets printed on stdout
                                while being executed
    @return                     stdout, stderr

    See notebook :ref:`csharpformlinnotebookrst`
    for an example.
    """
    AddReference('CSharPyMLExtension')
    from CSharPyMLExtension import PyMamlHelper
    if catch_output:
        res = PyMamlHelper.MamlAll(script, True)
        res = res.replace('\r', '')
        out, err = res.split('--ERR--')
        out = out.split('--OUT--')[-1]
        return out.strip(' \n\r'), err.strip(' \n\r')
    else:
        MamlHelper.MamlAll(script, False)
        return None, None


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
