# -*- coding: utf-8 -*-
import sys
import os
import shutil
import warnings
import re
from setuptools import setup, Extension
from setuptools import find_packages

#########
# settings
#########

project_var_name = "csharpyml"
project_owner = "sdpython"
sversion = "0.1"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = 'HISTORY.rst'


KEYWORDS = project_var_name + ', first name, last name'
DESCRIPTION = "Tools to use C# + Python mostly from Python."


CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]


#######
# data
#######


packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name + ".binaries": ["*.dll", "*.so"]}

############
# functions
############


def is_local():
    file = os.path.abspath(__file__).replace("\\", "/").lower()
    if "/temp/" in file and "pip-" in file:
        return False
    from pyquickhelper.pycode.setup_helper import available_commands_list
    return available_commands_list(sys.argv)


def ask_help():
    return "--help" in sys.argv or "--help-commands" in sys.argv


def verbose():
    print("---------------------------------")
    print("package_dir =", package_dir)
    print("packages    =", packages)
    print("package_data=", package_data)
    print("current     =", os.path.abspath(os.getcwd()))
    print("---------------------------------")

##########
# version
##########


if is_local() and not ask_help():
    def write_version():
        from pyquickhelper.pycode import write_version_for_setup
        return write_version_for_setup(__file__)

    write_version()

    versiontxt = os.path.join(os.path.dirname(__file__), "version.txt")
    if os.path.exists(versiontxt):
        with open(versiontxt, "r") as f:
            lines = f.readlines()
        subversion = "." + lines[0].strip("\r\n ")
        if subversion == ".0":
            raise Exception("Git version is wrong: '{0}'.".format(subversion))
    else:
        raise FileNotFoundError(versiontxt)
else:
    # when the module is installed, no commit number is displayed
    subversion = ""

if "upload" in sys.argv and not subversion and not ask_help():
    # avoid uploading with a wrong subversion number
    raise Exception(
        "Git version is empty, cannot upload, is_local()={0}".format(is_local()))

##############
# common part
##############

if os.path.exists(readme):
    with open(readme, "r", encoding='utf-8-sig') as f:
        long_description = f.read()
else:
    long_description = ""
if os.path.exists(history):
    with open(history, "r", encoding='utf-8-sig') as f:
        long_description += f.read()

if "--verbose" in sys.argv:
    verbose()

if is_local():
    from pyquickhelper import get_fLOG, get_insetup_functions
    logging_function = get_fLOG()
    logging_function(OutputPrint=True)
    must_build, run_build_ext = get_insetup_functions()

    if must_build():
        out = run_build_ext(__file__)
        print(out)

    from pyquickhelper.pycode import process_standard_options_for_setup
    r = process_standard_options_for_setup(
        sys.argv, __file__, project_var_name,
        extra_ext=["cs"],
        add_htmlhelp=sys.platform.startswith("win"),
        coverage_options=dict(omit=["*exclude*.py"]),
        github_owner=project_owner,
        fLOG=logging_function, covtoken=(
            "d911f0bb-f250-415d-860b-19b342a4f168", "'_UT_36_std' in outfile"),
        requirements=["pyquickhelper", "jyquickhelper"],
        additional_notebook_path=["pyquickhelper", "jyquickhelper"],
        additional_local_path=["pyquickhelper", "jyquickhelper"],
        copy_add_ext=["dll", 'so'], layout=["pdf", "html"])
    if not r and not ({"bdist_msi", "sdist",
                       "bdist_wheel", "publish", "publish_doc", "register",
                       "upload_docs", "bdist_wininst", "build_ext"} & set(sys.argv)):
        raise Exception("unable to interpret command line: " + str(sys.argv))
else:
    r = False


def build_machinelearning():
    "builds machinelearning"
    from pyquickhelper.loghelper import run_cmd
    print('[csharpyml.machinelearning]')
    this = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(this, 'cscode', 'machinelearning')
    cmd = "build{0}"
    if sys.platform.startswith("win"):
        cmd = cmd.format('.cmd')
    else:
        cmd = cmd.format('.sh')
    full = os.path.join(folder, cmd)
    if not os.path.exists(full):
        existing = os.listdir(folder)
        raise FileNotFoundError("Unable to find '{0}', build failed. Found:\n{1}".format(
                                full, "\n".join(existing)))
    if not sys.platform.startswith("win"):
        cmd = "bash --verbose " + cmd
    cmd += ' -Release'
    out, err = run_cmd(cmd, wait=True, change_path=folder)
    if len(err) > 0:
        # Filter out small errors.
        errs = []
        lines = err.split('\n')
        for line in lines:
            if 'ILAsmVersion.txt: No such file or directory' in line:
                continue
            errs.append(line)
        err = "\n".join(errs)
    if len(err) > 0:
        raise RuntimeError(
            "Unable to build machinelearning code.\nCMD: {0}\n--ERR--\n{1}".format(cmd, err))
    elif len(out) > 0:
        print('[csharpyml.dotnet] OUT')
        print(out)
    bin = os.path.join(folder, "bin")
    if not os.path.exists(bin):
        existing = os.listdir(folder)
        raise FileNotFoundError("Unable to find '{0}', build failed. Found:\n{1}".format(
                                bin, "\n".join(existing)))


def build_module():
    "build the module"
    # git submodule add https://github.com/dotnet/machinelearning.git cscode/machinelearning
    # We build a dotnet application.
    from pyquickhelper.loghelper import run_cmd

    env = os.environ.get('DOTNET_CLI_TELEMETRY_OPTOUT', None)
    if env is None:
        os.environ['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
    print('[csharpyml.env] DOTNET_CLI_TELEMETRY_OPTOUT={0}'.format(
        os.environ['DOTNET_CLI_TELEMETRY_OPTOUT']))

    # builds the other libraries
    cmds = ['dotnet restore CSharPyMLExtension_netcore.sln',
            'dotnet build --verbose -c Release CSharPyMLExtension_netcore.sln']
    folder = os.path.abspath("cscode")
    outs = []
    for cmd in cmds:
        out, err = run_cmd(cmd, fLOG=print, wait=True, change_path=folder)
        if len(err) > 0:
            raise RuntimeError(
                "Unable to compile C# code.\nCMD: {0}\n--ERR--\n{1}".format(cmd, err))
        elif len(out) > 0:
            outs.append(out)
            print('[csharpyml.dotnet] OUT')
            print(out)

    # Copy specific files.
    copy_assemblies()


def extract_version_target(path):
    "3.5.1/lib/netstandard1.0 --> (3, 5, 1), 'netstandard1.0')"
    reg = re.compile(
        '([0-9]+[.][0-9]+[.][0-9]+).*[/\\\\](netstandard[0-9][.][0-9])')
    res = reg.search(path)
    if res:
        g1, g2 = res.groups()
        if g1:
            g1 = tuple(int(_) for _ in g1.split('.'))
        else:
            g1 = None
        if not g2:
            g2 = None
        return g1, g2
    else:
        reg = re.compile('(netstandard[0-9][.][0-9])')
        res = reg.search(path)
        if res:
            return None, res.groups()[0]
        else:
            reg = re.compile('(netcoreapp[0-9][.][0-9])')
            res = reg.search(path)
            if res:
                return None, res.groups()[0]
            else:
                reg = re.compile('(Native)')
                res = reg.search(path)
                if res:
                    return None, res.groups()[0]
                else:
                    return None, None


def find_folder_package(folder):
    "Finds the best location within a package"
    from pyquickhelper.filehelper import explore_folder
    dirs, _ = explore_folder(folder)
    found = []
    for d in dirs:
        version, net = extract_version_target(d)
        if version is not None and net is not None:
            found.append((version, net, d))
        elif net is not None:
            found.append((None, net, d))
    if not found:
        raise FileNotFoundError("Not suitable path for '{0}'".format(folder))
    else:
        mx = max(found)
        return mx


def copy_assemblies(ml=False):
    "Copies all assemblies in the right location."
    from pyquickhelper.filehelper import synchronize_folder
    if ml:
        folders = ['cscode/machinelearning/packages/google.protobuf',
                   'cscode/machinelearning/packages/newtonsoft.json',
                   'cscode/machinelearning/packages/parquet.net',
                   'cscode/machinelearning/packages/system.reflection',
                   'cscode/machinelearning/bin/x64.Release/Native',
                   'cscode/machinelearning/bin/AnyCPU.Release/Microsoft.ML.Predictor.Tests',
                   ]
    else:
        folders = ['cscode/CSharPyMLExtension/bin/Release']
    dest = 'src/csharpyml/binaries'
    for fold in folders:
        v, n, found = find_folder_package(fold)
        if "packages" in fold:
            if v is None:
                raise FileNotFoundError(
                    "Unable to find a suitable version for package '{0}'".format(fold))
        elif 'Native' not in found and 'netcoreapp' not in found and 'netstandard' not in found:
            raise FileNotFoundError(
                "Unable to find a suitable folder binaries '{0}'".format(fold))
        print("[csharpyml.copy] '{0}' -> '{1}'".format(found, dest))
        synchronize_folder(found, dest, fLOG=print, no_deletion=True)


if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)

    from pyquickhelper.pycode import clean_readme
    long_description = clean_readme(long_description)
    root = os.path.abspath(os.path.dirname(__file__))
    end = False

    if "copybinml" in sys.argv:
        copy_assemblies(ml=True)
        end = True
    elif "copybin" in sys.argv:
        copy_assemblies(ml=False)
        end = True
    elif "build_ext" in sys.argv:
        if '--inplace' not in sys.argv:
            raise Exception("Option --inplace must be set up.")
        # builds machinelearning
        if '--submodules' in sys.argv:
            sys.argv = [_ for _ in sys.argv if _ != '--submodules']
            build_machinelearning()
            copy_assemblies(ml=True)
        build_module()
        copy_assemblies()

    if sys.platform.startswith("win"):
        extra_compile_args = None
    else:
        extra_compile_args = ['-std=c++11']

    if not end:
        # C parts
        ext_cparts = Extension('src.csharpyml.cparts.cmodule',
                               [os.path.join(root, 'src/csharpyml/cparts/version.cpp'),
                                   os.path.join(root, 'src/csharpyml/cparts/cmodule.cpp')],
                               extra_compile_args=extra_compile_args,
                               include_dirs=[os.path.join(root, 'src/csharpyml/cparts')])

        # Regular setup.
        setup(
            name=project_var_name,
            ext_modules=[ext_cparts],
            version='%s%s' % (sversion, subversion),
            author='Xavier Dupré',
            author_email='xavier.dupre@gmail.com',
            license="MIT",
            url="http://www.xavierdupre.fr/app/csharpyml/",
            download_url="https://github.com/sdpython/csharpyml/",
            description=DESCRIPTION,
            long_description=long_description,
            keywords=KEYWORDS,
            classifiers=CLASSIFIERS,
            packages=packages,
            package_dir=package_dir,
            package_data=package_data,
            # data_files=data_files,
            install_requires=['pythonnet', 'pyquickhelper'],
            # include_package_data=True,
        )
