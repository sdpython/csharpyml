"""
@file
@brief
"""
from clr import AddReference as ClrAddReference


def AddReference(name):
    """
    Imports a :epkg:`C#` dll.
    """
    try:
        return ClrAddReference(name)
    except Exception as e:
        if "Unable to find assembly" in str(e):
            import sys
            import os
            this = os.path.abspath(os.path.dirname(__file__))
            if this and os.path.exists(this):
                sys.path.append(this)
                try:
                    res = ClrAddReference(name)
                except Exception:
                    del sys.path[-1]
                    raise
                del sys.path[-1]
                return res
            else:
                raise
        else:
            raise


def add_csharpml_extension():
    """
    Imports *CSharpExtension* into global context.

    This binary has a version. On :epkg:`Windows`,
    the system might decide to skip the replacement
    of an assembly because it is in use. You can
    check the version of this by using the following code.

    .. exref::
        :title: Imports the C# extension into :pekg:`Python`

        .. runpython::
            :showcode:

            from csharpyml.binaries import add_csharpml_extension
            from csharpyml import __version__

            add_csharp_extension()

            # This line needs to be after the previous one.
            from CSharPyMLExtension import Constants

            vers = Constants.Version()
            print(__version__, vers)
    """
    AddReference("CSharPyMLExtension")
