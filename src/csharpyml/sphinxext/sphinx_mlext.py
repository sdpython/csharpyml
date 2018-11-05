"""
@file
@brief Extends :epkg:`Sphinx` to easily write documentation with :epkg:`ML.net`.
"""
import os
import jinja2
import sphinx
from sphinx.util import logging
from pyquickhelper.sphinxext.sphinx_runpython_extension import RunPythonDirective
from csharpy.sphinxext import RunCSharpDirective
from ..binaries import get_maml_helper


def maml_pythonnet(script, verbose=2):
    """
    Runs a *maml script* through :epkg:`ML.net`.

    @param      script          script
    @param      verbose         adjust the verbosity
    @return                     stdout and stderr
    """
    res = get_maml_helper().MamlScriptConsole(script, True, verbose)
    return res


def maml_test():
    """
    Tests the assembly.
    """
    get_maml_helper().TestScikitAPI()
    get_maml_helper().TestScikitAPI2()
    iris = os.path.abspath(os.path.join(os.path.dirname(__file__), "iris.txt"))
    if not os.path.exists(iris):
        raise FileNotFoundError("Unable to find '{0}'.".format(iris))
    get_maml_helper().TestScikitAPITrain(iris)


class MlCmdDirective(RunPythonDirective):
    """
    Runs a command line based on :epkg:`ML.net`.
    """

    def modify_script_before_running(self, script):
        """
        The methods modifies ``self.content``.
        """
        script = ["from textwrap import dedent",
                  "from sphinx_mlext import maml_pythonnet",
                  "content = dedent('''",
                  script,
                  "''')"
                  "",
                  "out = maml_pythonnet(content)",
                  "print(out)",
                  ]
        return "\n".join(script)


def mlnet_components_kinds():
    """
    Retrieves all kinds.
    """
    MamlHelper = get_maml_helper()
    kinds = list(MamlHelper.GetAllKinds())
    kinds += ["argument", "command"]
    kinds = list(set(kinds))
    titles = {
        'anomalydetectortrainer': 'Anomaly Detection',
        'binaryclassifiertrainer': 'Binary Classification',
        'clusteringtrainer': 'Clustering',
        'dataloader': 'Data Loader',
        'datasaver': 'Data Saver',
        'datascorer': 'Scoring',
        'datatransform': 'Transforms (all)',
        'ensembledataselector': 'Data Selection',
        'evaluator': 'Evaluation',
        'multiclassclassifiertrainer': 'Multiclass Classification',
        'ngramextractorfactory': 'N-Grams',
        'rankertrainer': 'Ranking',
        'regressortrainer': 'Regression',
        'tokenizetransform': 'Tokenization',
        'argument': 'Arguments',
        'command': 'Commands',
    }
    return {k: titles[k] for k in kinds if k in titles}


def builds_components_pages(epkg):
    """
    Returns components pages.

    @param  epkg        dictionary used to replace substrings by hyperlinks
    @return             list of modified pages
    """
    try:
        from .sphinx_mlext_templates import index_template, kind_template, component_template
    except (ModuleNotFoundError, ImportError):
        from sphinx_mlext_templates import index_template, kind_template, component_template
    try:
        from .machinelearning_docs import components
    except (ModuleNotFoundError, ImportError):
        from machinelearning_docs import components
    try:
        from pyquickhelper.texthelper import add_rst_links
    except ImportError:
        logger = logging.getLogger("csml")
        logger.warning("[csml] update pyquickhelper to a newer version.")

    if "OPTICS" not in epkg:
        raise KeyError("OPTICS not found in epkg")

    def process_default(default_value):
        if not default_value:
            return ''
        if "+" in default_value:
            default_value = default_value.split(".")[-1].replace("+", ".")
            return default_value
        if len(default_value) > 28:
            if len(default_value.split(".")) > 2:
                default_value = default_value.replace(".", ". ")
            elif len(default_value.split(",")) > 2:
                default_value = default_value.replace(",", ", ")
            else:
                raise ValueError("Unable to shorten default value '{0}' len={1}.".format(
                    default_value, len(default_value)))
        return default_value

    def process_description(desc):
        if desc is None:
            return ''
        if not isinstance(desc, str):
            raise TypeError("desc must be a string not {0}".format(type(desc)))
        return add_rst_links(desc, epkg)

    def clean_name(name):
        return name.replace(" ", "_").replace(".", "_").replace("(", "").replace(")", "").lower()

    kinds = mlnet_components_kinds()
    pages = {}

    # index
    sorted_kinds = list(sorted((v, k) for k, v in kinds.items()))
    template = jinja2.Template(index_template)
    pages["index"] = template.render(sorted_kinds=sorted_kinds)

    kind_tpl = jinja2.Template(kind_template)
    comp_tpl = jinja2.Template(component_template)
    logger = logging.getLogger("csml")

    MamlHelper = get_maml_helper()

    # builds references
    refs = {}
    for v, k in sorted_kinds:
        enumc = MamlHelper.EnumerateComponents(k)
        try:
            comps = list(enumc)
        except Exception as e:  # pylint: disable=W0703
            logger.warning("[csml] issue with kind {0}\n{1}".format(k, e))
            continue
        if len(comps) == 0:
            logger.warning("[csml] empty kind {0}\n{1}".format(k, e))
            continue
        for comp in comps:
            refs[comp.Name] = ":ref:`l-{0}`".format(
                comp.Name.lower().replace(".", "-"))

    # kinds and components
    for v, k in sorted_kinds:
        enumc = MamlHelper.EnumerateComponents(k)
        try:
            comps = list(enumc)
        except Exception as e:  # pylint: disable=W0703
            logger.warning("[csml] issue with kind {0}\n{1}".format(k, e))
            continue
        if len(comps) == 0:
            logger.warning("[csml] empty kind {0}\n{1}".format(k, e))
            continue

        comp_names = list(sorted(clean_name(c.Name) for c in comps))
        kind_name = v
        kind_kind = k
        pages[k] = kind_tpl.render(title=kind_name, fnames=comp_names, len=len)

        for comp in comps:

            if comp.Arguments is None and "version" not in comp.Name.lower():
                logger.info(
                    "[csml] ---- SKIP ---- {}-{}-{}".format(k, comp.Name, comp.Description))
            else:
                assembly_name = comp.AssemblyName
                args = {}
                if comp.Arguments is not None:
                    for arg in comp.Arguments:
                        dv = process_default(arg.DefaultValue)
                        args[arg.Name] = dict(Name=arg.Name, ShortName=arg.ShortName or '',
                                              Default=refs.get(dv, dv), Description=arg.Help)
                sorted_params = [v for k, v in sorted(args.items())]
                aliases = ", ".join(comp.Aliases)

                if assembly_name.startswith("Microsoft.ML"):
                    linkdocs = "**Microsoft Documentation:** `{0} <https://docs.microsoft.com/dotnet/api/{1}.{2}>`_"
                    linkdocs = linkdocs.format(
                        comp.Name, comp.Namespace.lower(), comp.Name.lower())
                else:
                    linkdocs = ""

                comp_name = clean_name(comp.Name)
                pages[comp_name] = comp_tpl.render(title=comp.Name,
                                                   aliases=aliases,
                                                   summary=process_description(
                                                       comp.Description),
                                                   kind=kind_kind,
                                                   namespace=comp.Namespace,
                                                   sorted_params=sorted_params,
                                                   assembly=assembly_name,
                                                   len=len, linkdocs=linkdocs,
                                                   docadd=components.get(
                                                       comp.Name, ''),
                                                   MicrosoftML="Microsoft.ML" in assembly_name,
                                                   ScikitML="Scikit.ML" in assembly_name)
    return pages


def write_components_pages(app, env, docnames):
    """
    Writes documentation pages.
    """
    pages = builds_components_pages(app.config.epkg_dictionary)
    docdir = env.srcdir
    dest = os.path.join(docdir, "components")
    if not os.path.exists(dest):
        os.mkdir(dest)
    for k, v in pages.items():
        d = os.path.join(dest, k) + ".rst"
        if os.path.exists(d):
            with open(d, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = None

        if content != v:
            with open(d, "w", encoding="utf-8") as f:
                f.write(v)


class RunCSharpMLDirective(RunCSharpDirective):  # pylint: disable=E0602
    """
    Implicits "and dependencies.
    """

    def modify_script_before_running(self, script):
        """
        The methods modifies the script to *csharpy* to
        run :epkg:`C#` from :epkg:`Python`.
        """
        if not hasattr(RunCSharpDirective, 'deps_using'):  # pylint: disable=E0602
            RunCSharpDirective.deps_using = get_mlnet_assemblies()  # pylint: disable=E0602
        dependencies, usings = RunCSharpMLDirective.deps_using
        return self._modify_script_before_running(script, usings, dependencies)


def setup(app):
    """
    Adds the custom directive.
    """
    app.add_directive('mlcmd', MlCmdDirective)
    app.connect("env-before-read-docs", write_components_pages)
    app.add_directive('runcsharpml', RunCSharpMLDirective)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
