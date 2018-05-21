# -*- coding: utf-8 -*-
"""
@file
@brief Defines magic commands to interact with C# in a :epkg:`Python` notebook.
"""
from IPython.core.magic import magics_class, cell_magic
from pyquickhelper.ipythonhelper import MagicCommandParser, MagicClassWithHelpers
from ..binaries import maml


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


def register_magics(ip):
    """
    Registers magics commands.
    """
    ip.register_magics(CsMLMagics)
