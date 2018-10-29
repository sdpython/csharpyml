import sys
import os
import sphinx_gallery
# import sphinx_rtd_theme
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "csharpyml", "sdpython", 2018,
                     "alabaster", [alabaster.get_path()],
                     locals(), book=True,
                     extlinks=dict(issue=('https://github.com/sdpython/csharpyml/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/csharpyml/helpsphinx/"

extensions.extend(['csharpyml.sphinxext.sphinx_mlext'])

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css', '_static/gallery.css'],
}

nblinks = {'slideshowrst': 'http://www.xavierdupre.fr/'}


def custom_latex_processing(latex):
    """
    Processes a :epkg:`latex` file and returned the modified version.

    @param      latex       string
    @return                 string
    """
    if latex is None:
        raise ValueError("Latex is null")
    # this weird modification is only needed when jenkins run a unit test in
    # pyquickhelper (pycode)
    return latex


epkg_dictionary.update({
    'C#': 'https://en.wikipedia.org/wiki/C_Sharp_(programming_language)',
    'C# Streaming DataFrame': 'https://github.com/sdpython/machinelearningext/blob/master/machinelearningext/DataManipulation/StreamingDataFrame.cs',
    'C# DataFrame': 'https://github.com/sdpython/machinelearningext/blob/master/machinelearningext/DataManipulation/DataFrame.cs',
    'C# IDataView': 'https://github.com/dotnet/machinelearning/blob/master/src/Microsoft.ML.Core/Data/IDataView.cs',
    'C# LogWriter': 'https://github.com/xadupre/machinelearningext/blob/master/machinelearningext/PipelineHelper/DelegateEnvironment.cs',
    'C# Pipeline': 'https://github.com/sdpython/machinelearningext/blob/master/machinelearningext/ScikitAPI/ScikitPipeline.cs',
    'C# ScikitPipeline': 'https://github.com/xadupre/machinelearningext/blob/master/machinelearningext/ScikitAPI/ScikitPipeline.cs',
    'csv': 'https://en.wikipedia.org/wiki/Comma-separated_values',
    'DataFrame': 'https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html',
    'DataKind': 'https://github.com/dotnet/machinelearning/blob/master/src/Microsoft.ML.Core/Data/DataKind.cs#L13',
    'DBSCAN': 'https://en.wikipedia.org/wiki/DBSCAN',
    'dotnet/machinelearning': 'https://github.com/dotnet/machinelearning',
    'LightGBM': 'https://github.com/Microsoft/LightGBM',
    'MIT License': 'https://github.com/dotnet/machinelearning/blob/master/LICENSE',
    'ML.net': 'https://github.com/dotnet/machinelearning',
    'OPTICS': 'https://en.wikipedia.org/wiki/OPTICS_algorithm',
    'Scikit.ML': 'https://github.com/xadupre/machinelearningext',
    'Scikit.ML Documentation': 'http://www.xavierdupre.fr/app/machinelearningext/helpsphinx/index.html',
    'Windows': 'https://www.microsoft.com/',
    'xadupre/machinelearningext': 'https://github.com/xadupre/machinelearningext',
})

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

from recommonmark.parser import CommonMarkParser
source_parsers = {'.md': CommonMarkParser}
source_suffix = ['.rst', '.md']
