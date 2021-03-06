# -*- coding: utf-8 -*-
"""
@file
@brief Defines magic commands to interact with C# in a :epkg:`Python` notebook.
"""
from IPython.core.magic import magics_class, cell_magic
from pyquickhelper.ipythonhelper import MagicCommandParser, MagicClassWithHelpers
from csharpy.notebook.csmagics import CsMagics
from ..binaries import maml, mlnet


@magics_class
class CsMLMagics(MagicClassWithHelpers):
    """
    Defines magic commands for notebooks.
    """

    @staticmethod
    def maml_parser():
        """
        Defines the way to parse the magic command ``%%maml``.
        """
        parser = MagicCommandParser(prog="maml",
                                    description='Runs a maml script.')
        parser.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='hide output')
        return parser

    @cell_magic
    def maml(self, line, cell):
        """
        Defines magic command ``%%maml``.

        .. nbref::
            :title: %%maml
            :lid: cmagic-maml

            The magic command wraps the function @see fn maml.

            ::

                %%maml

                data=iris.txt
                loader=text{col=Label:U4[0-2]:0 col=Slength:R4:1 col=Swidth:R4:2
                            col=Plength:R4:3 col=Pwidth:R4:4 sep=, header=+}
                xf=Concat{col=Features:Slength,Swidth}
                tr=ova{p=lr}
                out=model.zip
        """
        parser = self.get_parser(CsMLMagics.maml_parser, "maml")
        args = self.get_args(line, parser)

        if args is not None:
            quiet = args.quiet
            out, err = maml(cell, not quiet)
            if out:
                print(out)
            if err:
                print('-----')
                print(err)

    @staticmethod
    def mlnet_parser():
        """
        Defines the way to parse the magic command ``%%mlnet``.
        """
        parser = MagicCommandParser(prog="mlnet",
                                    description='Compiles and wrap a C# function into a Python function.\n'
                                                'Automatically adds ML.net dependencies.')
        parser.add_argument('name', type=str, help='function name')
        parser.add_argument('-i', '--idep', nargs='*', action='append',
                            help='internal dependencies (like System, System.Linq)')
        parser.add_argument('-d', '--dep', nargs='*', action='append',
                            help='dependencies (assembly name without extension)')
        parser.add_argument('-c', '--catch', action='store', default=False,
                            help='catch exception')
        return parser

    @cell_magic
    def mlnet(self, line, cell):
        """
        Defines magic command ``%%mlnet``.
        Relies on magic command :epkg:`%%CS`.

        .. nbref::
            :title: %%mlnet
            :lid: cmagic-mlnet

            The magic command wraps the function @see fn mlnet.

            ::

                %%mlnet

        """
        line, cell = CsMagics._preprocess_line_cell_maml(  # pylint: disable=W0212
            line, cell)

        parser = self.get_parser(CsMagics.CS_parser, "CS")
        args = self.get_args(line, parser)

        if args is not None:
            name = args.name
            dep = CsMagics._linearise_args(args.dep)  # pylint: disable=W0212
            idep = CsMagics._linearise_args(args.idep)  # pylint: disable=W0212

            if args.catch:
                try:
                    f = mlnet(name, cell, idep, dep)
                except Exception as e:  # pylint: disable=W0703
                    print(str(e).replace('\r', ''))
                    return None
            else:
                f = mlnet(name, cell, idep, dep)
            if self.shell is not None:
                self.shell.user_ns[name] = f
            return f
        return None


def register_magics(ip):
    """
    Registers magics commands.
    """
    ip.register_magics(CsMLMagics)
