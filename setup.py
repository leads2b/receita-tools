from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import receita


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    # Basic info
    name='receita',
    version=receita.__version__,
    url='http://github.com/vkruoso/receita-tools',
    license='Apache Software License',
    author='Vinicius K. Ruoso',
    author_email='vinicius.ruoso@gmail.com',
    description="Tools to manipulate Receita's company data.",

    # Details
    packages=['receita', 'receita.tools'],
    include_package_data=True,
    platforms='any',
    install_requires=[''],

    # Testing
    tests_require=['tox'],
    cmdclass = {'test': Tox},

    # # Scripts
    # entry_points={
    #     'console_scripts': [
    #         'foo = my_package.some_module:main_func',
    #         'bar = other_module:some_func',
    #     ],
    #     'gui_scripts': [
    #         'baz = my_package_gui:start_func',
    #     ]
    # }

    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        # 'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
