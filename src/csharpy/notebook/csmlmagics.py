# -*- coding: utf-8 -*-
"""
@file
@brief Defines magic commands to interact with C# in a :epkg:`Python` notebook.
"""
from IPython.display import Javascript
from IPython.core.magic import magics_class, cell_magic
from pyquickhelper.ipythonhelper import MagicCommandParser, MagicClassWithHelpers
from ..runtime import create_cs_function


@magics_class
class CsMagics(MagicClassWithHelpers):
    """
    Defines magic commands for notebooks.
    """

    @staticmethod
    def CS_parser():
        """
        Defines the way to parse the magic command ``%%CS``.
        """
        parser = MagicCommandParser(prog="CS",
                                    description='Compiles and wrap a C# function into a Python function.')
        parser.add_argument('name', type=str, help='function name')
        parser.add_argument('-i', '--idep', nargs='*', action='append',
                            help='internal dependencies (like System, System.Linq)')
        parser.add_argument('-d', '--dep', nargs='*', action='append',
                            help='dependencies (assembly name without extension)')
        parser.add_argument('-c', '--catch', action='store', default=False,
                            help='catch exception')
        return parser

    @cell_magic
    def CS(self, line, cell):
        """
        Defines magic command ``%%CS``.

        .. nbref::
            :title: %%CS

            The magic command wraps the :epkg:`C#` code into a
            :epkg:`Python` function the user can call.

            ::

                %%CS cspower -i System
                public static double cspower(double x, double y)
                {
                    if (y == 0) return 1.0 ;
                    return System.Math.Pow(x,y) ;
                }

            To call it:

            ::

                cspower(3.0, 3.0)

            The magic command relies on @see fn create_cs_function
            and adds it to the notebook context. Dependencies are usually
            specified on the first line. However, it is quite inconvenient
            to have a very long first line so the first cell line of the
            cell will be seen as a continuation if they start by ``-``
            like follows:

            ::

                %%CS cspower
                -i System
                public static double cspower(double x, double y)
                {
                    if (y == 0) return 1.0 ;
                    return System.Math.Pow(x,y) ;
                }
        """
        cell_lines = cell.split('\n')
        last = 0
        for i, li in enumerate(cell_lines):
            if not li.strip():
                continue
            if not li.startswith('-'):
                last = i
                break

        if last > 0:
            line += ' ' + ' '.join(cell_lines[:last])
            cell = "\n".join(cell_lines[last:])

        parser = self.get_parser(CsMagics.CS_parser, "CS")
        args = self.get_args(line, parser)

        def linearise(ll):
            "list of lists into list"
            if ll is None:
                return None
            res = []
            for el in ll:
                if isinstance(el, list):
                    res.extend(el)
                else:
                    res.append(el)
            return res

        if args is not None:
            name = args.name
            dep = linearise(args.dep)
            idep = linearise(args.idep)

            if args.catch:
                try:
                    f = create_cs_function(name, cell, idep, dep)
                except Exception as e:
                    print(str(e).replace('\r', ''))
                    return None
            else:
                f = create_cs_function(name, cell, idep, dep)
            if self.shell is not None:
                self.shell.user_ns[name] = f
            return f
        return None


def register_magics(ip):
    """
    Registers magics commands.
    """
    ip.register_magics(CsMagics)
    patch = ("IPython.config.cell_magic_highlight['csmagic'] = "
             "{'reg':[/^%%CS/]};")
    Javascript(data=patch, lib=[
               "https://github.com/codemirror/CodeMirror/blob/master/mode/clike/clike.js"])
