"""
@file
@brief Implements function around :epkg:`ML.net` command line.
"""
from .add_reference import AddReference


def maml(script, catch_output=True):
    """
    Runs a maml_script through :epkg:`ML.net`.

    @param      script          script
    @param      catch_output    the function returns the output as a result at of the
                                execution, otherwise, it gets printed on stdout
                                while being executed
    @return                     stdout, stderr
    """
    AddReference('CSharPyMLExtension')
    from CSharPyMLExtension import MamlHelper
    if catch_output:
        res = MamlHelper.MamlAll(script, True)
        res = res.replace('\r', '')
        out, err = res.split('--ERR--')
        out = out.split('--OUT--')[-1]
        return out.strip(' \n\r'), err.strip(' \n\r')
    else:
        MamlHelper.MamlAll(script, False)
        return None, None
