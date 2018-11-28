"""
@file
@brief Implements function around :epkg:`ML.net` command line.
"""
import os
from csharpy.runtime import create_cs_function
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


def get_mlnet_assemblies(chdir=False):
    """
    Makes the list required dependencies to run a C# script using :epkg:`ML.net`.

    @param      chdir       change directory to the current one before computing the list
    @return                 list of assemblies, list of usings

    .. runpython::
        :showcode:

        from csharpyml.binaries import get_mlnet_assemblies
        deps, usings = get_mlnet_assemblies()

        for i, d in enumerate(deps):
            print("dependencies %d: %s" % (i, d))
        for i, u in enumerate(usings):
            print("using %d: %s" % (i, u))
    """
    if chdir:
        cur = os.getcwd()
        os.chdir(chdir)
    MamlHelper = get_maml_helper()
    res = MamlHelper.GetLoadedAssembliesLocation(True)  # pylint: disable=E0602
    if chdir:
        os.chdir(cur)
    dependencies = []
    # addition = ["Core", "Data", "Maml", "Api"]
    # root = os.path.dirname(res[0].Location)
    # dependencies = [os.path.join(root, "Microsoft.ML.{0}.dll").format(a) for a in addition]
    dependencies.extend([a for a in res if ".pyd" not in a and ".so" not in a])
    usings = ["System", "System.Linq", "System.Collections.Generic", "System.IO",
              "System.Text"]
    usings.extend([
        "Microsoft.ML",
        "Microsoft.ML.Runtime",
        "Microsoft.ML.Runtime.Api",
        "Microsoft.ML.Runtime.Data",
        "Microsoft.ML.Runtime.Learners",
        "Microsoft.ML.Runtime.Ensemble",
        "Microsoft.ML.Runtime.LightGBM",
        "Microsoft.ML.Runtime.Model.Onnx",
        "Microsoft.ML.Runtime.TimeSeriesProcessing",
        "Microsoft.ML.Runtime.Tools",
        "Microsoft.ML.Trainers",
        "Microsoft.ML.Trainers.HalLearners",
        "Microsoft.ML.Trainers.KMeans",
        "Microsoft.ML.Trainers.FastTree",
        "Microsoft.ML.Trainers.Online",
        "Microsoft.ML.Trainers.PCA",
        "Microsoft.ML.Transforms",
        "Microsoft.ML.Transforms.Categorical",
        "Microsoft.ML.Transforms.Normalizers",
        "Microsoft.ML.Transforms.Projections",
        "Microsoft.ML.Transforms.TensorFlow",
        "Microsoft.ML.Transforms.Text",
        "Microsoft.ML.Runtime.Sweeper",
    ])
    res = MamlHelper.GetAssemblies()  # pylint: disable=E0602
    usings.extend([a.FullName.split(',')[0]
                   for a in res if "Scikit" in a.FullName])
    for miss in ["Scikit.ML.DataManipulation", "Scikit.ML.ScikitAPI"]:
        if miss not in usings:
            usings.append(miss)
    return dependencies, usings


def mlnet(name, code, usings=None, dependencies=None, redirect=False):
    """
    Compiles a :epkg:`C#` function using :epkg:`ML.net`.
    It automatically adds the necessary dependencies including
    in this package.
    Relies on :epkg:`create_cs_function`

    @param      name            function name
    @param      code            :epkg:`C#` code
    @param      usings          *using* to add, such as *System*, *System.Linq*, ...
    @param      dependencies    dependencies, can be absolute path file
    @param      redirect        redirect standard output and error
    @return                     :epkg:`Python` wrapper on the compiled :epkg:`C#`

    The default dependencies are returned by @see fn get_mlnet_assemblies.
    """
    deps, us = get_mlnet_assemblies()
    if usings is not None:
        us.extend(usings)
    if dependencies is not None:
        deps.extend(dependencies)
    return create_cs_function(name, code, us, deps, redirect)
