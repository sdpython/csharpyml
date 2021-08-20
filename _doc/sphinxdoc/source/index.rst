
csharpyml
=========

.. only:: html

    .. image:: https://travis-ci.com/sdpython/csharpyml.svg?branch=master
        :target: https://app.travis-ci.com/github/sdpython/csharpyml
        :alt: Build status

    .. image:: https://ci.appveyor.com/api/projects/status/ldrgt6sxeyfwtoo2?svg=true
        :target: https://ci.appveyor.com/project/sdpython/csharpyml
        :alt: Build Status Windows

    .. image:: https://circleci.com/gh/sdpython/csharpyml/tree/master.svg?style=svg
        :target: https://circleci.com/gh/sdpython/csharpyml/tree/master

    .. image:: https://badge.fury.io/py/csharpyml.svg
        :target: http://badge.fury.io/py/csharpyml

    .. image:: http://img.shields.io/github/issues/sdpython/csharpyml.png
        :alt: GitHub Issues
        :target: https://github.com/sdpython/csharpyml/issues

    .. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :alt: MIT License
        :target: http://opensource.org/licenses/MIT

    .. image:: https://codecov.io/github/sdpython/csharpyml/coverage.svg?branch=master
        :target: https://codecov.io/github/sdpython/csharpyml?branch=master

.. image:: nbcov.png
    :target: http://www.xavierdupre.fr/app/csharpyml/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

**Links:** `github <https://github.com/sdpython/csharpyml/>`_,
`documentation <http://www.xavierdupre.fr/app/csharpyml/helpsphinx2/index.html>`_
:ref:`l-README`,
:ref:`blog <ap-main-0>`

What is it?
-----------

*csharpyml* implements a way to interact
with :epkg:`C#` and :epkg:`ML.net` from :epkg:`Python`.
The module relies on `pythonnet <https://github.com/pythonnet/pythonnet>`_,
wraps :epkg:`ML.net` and :epkg:`Scikit.ML`
(see also :epkg:`Scikit.ML Documentation`).

Documentation
-------------

.. toctree::
    :maxdepth: 2

    api/index
    components/index
    examples
    i_faq
    i_nb
    blog/blogindex
    indexmenu
    HISTORY
    license

It can easily compile and wrap a :epkg:`C#` function
into :epkg:`Python`:

.. runpython::
    :showcode:

    from csharpyml.binaries import maml
    print(maml('?')[0])

The list of available trainers can be obtained with:

.. runpython::
    :showcode:

    from csharpyml.binaries import maml
    print(maml('? kind=trainer')[0])

This function also exists as a magic command
:ref:`%%maml <cmagic-maml>`.

Installation
------------

*Windows*

Follow the instructions described in
`appveyor.yml <https://github.com/sdpython/csharpyml/blob/master/appveyor.yml>`_.

*Linux*

Follow the instructions described in
`config.yml <https://github.com/sdpython/csharpyml/blob/master/.circleci/config.yml>`_.

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-EX2`       | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ2`      | :ref:`l-notebooks`  | :ref:`l-HISTORY`   | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
