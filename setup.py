# -*- coding: utf-8 -*-
import sys
import os
import shutil
import warnings
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

if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)
    from pyquickhelper.pycode import clean_readme
    long_description = clean_readme(long_description)
    root = os.path.abspath(os.path.dirname(__file__))

    if "build_ext" in sys.argv:
        
        from pyquickhelper.loghelper import run_cmd
        
        def build_machinelearning():
            "builds machine learning"
            print('[csharpyml.machinelearning]')
            this = os.path.dirname(__file__)
            folder = os.path.join(this, 'cscode', 'machinelearning')
            cmd = "build -Release"
            out, err = run_cmd(cmd, wait=True, change_path=folder)
            if len(err) > 0:
                raise RuntimeError(
                    "Unable to build machinelearning code.\nCMD: {0}\n--ERR--\n{1}".format(cmd, err))
            elif len(out) > 0:
                print('[csharpyml.dotnet] OUT')
                print(out)                
        
        # git submodule add https://github.com/dotnet/machinelearning.git cscode/machinelearning
        # We build a dotnet application.
        if '--inplace' not in sys.argv:
            raise Exception("Option --inplace must be set up.")
        
        env = os.environ.get('DOTNET_CLI_TELEMETRY_OPTOUT', None)
        if env is None:
            os.environ['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
        print('[csharpyml.env] DOTNET_CLI_TELEMETRY_OPTOUT={0}'.format(
            os.environ['DOTNET_CLI_TELEMETRY_OPTOUT']))
            
        # builds machinelearning
        build_machinelearning()
        
        # builds the other libraries
        cmds = ['dotnet restore CSharPyMLExtension_netcore.sln',
                'dotnet build -c Release CSharPyMLExtension_netcore.sln']
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

        # Copy files.
        from pyquickhelper.filehelper import explore_folder_iterfile
        dest = os.path.join('src', 'csharpyml', 'binaries')
        must_copy = {'CSharPyMLExtension': 0}
        copied = 0
        for name in explore_folder_iterfile(folder, pattern='.*[.]((dll)|(so))$'):
            full = os.path.join(folder, name)
            if 'Release' in full:
                short_name = os.path.split(os.path.splitext(name)[0])[-1]
                if short_name in must_copy:
                    must_copy[short_name] += 1
                copied += 1
                print("[csharpyml.copy] '{0}'".format(name))
                shutil.copy(name, dest)
            else:
                print("[csharpyml.skip] '{0}'".format(name))
        min_must_copy = min(must_copy.values())
        if copied == 0 or min_must_copy == 0:
            raise RuntimeError("Missing binaries in '{0}'".format(folder))

    if sys.platform.startswith("win"):
        extra_compile_args = None
    else:
        extra_compile_args = ['-std=c++11']

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
