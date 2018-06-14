"""
@brief      test log(time=0s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_style_src(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C011111'),
                   skip=["Unable to import 'CSharPyExtension'",
                         "Unable to import 'System'",
                         "Module 'clr' has no 'AddReference' member",
                         "Unable to import 'System.Collections.Generic'",
                         "Unable to import 'DynamicCS'",
                         "No name 'AddReference' in module 'clr'",
                         "csmagics.py:113: W0703",
                         "add_reference.py:14: W0703",
                         "No name 'version_c' in module 'src.csharpyml.cparts.cmodule'",
                         "Unable to import 'CSharPyMLExtension'",
                         ])

    def test_style_test(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0703'),
                   skip=["src' imported but unused",
                         "skip_' imported but unused",
                         "skip__' imported but unused",
                         "skip___' imported but unused",
                         "Unused variable 'skip_'",
                         "imported as skip_",
                         "Unused import src",
                         "Unused import clr",
                         "Unable to import 'CSharPyMLExtension'",
                         "Unable to import 'System'",
                         "Module 'clr' has no 'AddReference' member",
                         "Unable to import 'System.Collections.Generic'",
                         "Instance of 'tuple' has no 'target' member",
                         "Instance of 'tuple' has no 'data' member",
                         'if __name__ == "__main__":',
                         ])


if __name__ == "__main__":
    unittest.main()
