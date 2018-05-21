"""
@file
@brief Module *python3_module_template*.
Empty module, template for others.
"""

__version__ = "0.1"
__author__ = "sdpython"
__github__ = "https://github.com/sdpython/csharpyml"
__url__ = "http://www.xavierdupre.fr/app/csharpyml/helpsphinx/index.html"
__downloadUrl__ = "https://github.com/sdpython/csharpyml"
__license__ = "MIT License"
__blog__ = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>blog</title>
    </head>
    <body>
        <outline text="csharpyml"
            title="csharpyml"
            type="rss"
            xmlUrl="http://www.xavierdupre.fr/app/csharpyml/helpsphinx/_downloads/rss.xml"
            htmlUrl="http://www.xavierdupre.fr/app/csharpyml/helpsphinx/blog/main_0000.html" />
    </body>
</opml>
"""


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.
    If you want to disable the logs:

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True


def _setup_hook(use_print=False):
    """
    if this function is added to the module,
    the help automation and unit tests call it first before
    anything goes on as an initialization step.
    """
    # we can check many things, needed module
    # any others things before unit tests are started
    if use_print:
        print("Success: _setup_hook")


def load_ipython_extension(ip):
    """
    to allow the call ``%load_ext csharpy``

    @param      ip      from ``get_ipython()``
    """
    from .notebook import register_magics
    register_magics(ip)
