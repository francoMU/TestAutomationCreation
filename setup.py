import os
import subprocess
import sysconfig

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

from pathlib import Path


class CustomBuildExtCommand(build_ext):

    def run(self):

        print("*"*20)

        full_path = os.path.realpath(__file__)
        exe_dir = os.path.dirname(full_path)

        print("*"*20)

        command = "git submodule update --init --recursive"
        process = subprocess.Popen(command, shell=True, cwd=exe_dir)
        process.wait()

        build_ext.run(self)

config_var = sysconfig.get_config_var("CFLAGS")
if (config_var is not None and
    "-Werror=declaration-after-statement" in config_var):
    os.environ['CFLAGS'] = config_var.replace(
        "-Werror=declaration-after-statement", "")


sources = ['arithmetic.c',
           'cell.c',
           'delaunay.c',
           'debug.c',
           'determination.c',
           'hall_symbol.c',
           'kgrid.c',
           'kpoint.c',
           'mathfunc.c',
           'niggli.c',
           'overlap.c',
           'pointgroup.c',
           'primitive.c',
           'refinement.c',
           'sitesym_database.c',
           'site_symmetry.c',
           'spacegroup.c',
           'spin.c',
           'spg_database.c',
           'spglib.c',
           'symmetry.c']


source_dir = "spglib/src"

include_dirs = [source_dir, ]

sources_full_path = [Path(source_dir) / file for file in source_dir]

extra_compile_args = []
extra_link_args = []
define_macros = []

extension = Extension('spglib._spglib',
                      include_dirs=include_dirs,
                      sources=sources,
                      extra_compile_args=extra_compile_args,
                      extra_link_args=extra_link_args,
                      define_macros=define_macros)


setup(
    name='spglibtricks',
    version='0.1',
    packages=['spglibtricks'],
    install_requires=[
        'numpy'
    ],
    cmdclass=dict(build_ext=CustomBuildExtCommand),
    zip_safe=False,
    include_package_data=True,
    ext_modules=[extension],
)
