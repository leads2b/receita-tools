from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
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
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


curdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(curdir, 'README.rst')) as readme:
    long_description = readme.read()

setup(
    # Basic info
    name='receita-tools',
    version=receita.__version__,
    url='http://github.com/vkruoso/receita-tools',
    license='MIT License',
    author='Vinicius K. Ruoso',
    author_email='vinicius.ruoso@gmail.com',
    description="Tools to manipulate Receita's company data.",
    long_description=long_description,

    # Details
    packages=['receita', 'receita.tools'],
    include_package_data=True,
    platforms='any',

    # On TLSv1.2 support:
    # https://github.com/kennethreitz/requests/blob/master/requests/packages/urllib3/contrib/pyopenssl.py
    # https://github.com/kennethreitz/requests/issues/3006
    # We are supporting TLSv1 for now, so it is not essential to have these
    # packages, but it is good to be prepared.
    install_requires=[
        'requests',
        'pyOpenSSL',  # needed for SSL support
        'ndg-httpsclient',  # needed for SSL support
        'pyasn1',   # needed for SSL support
        'unicodecsv',
        'progressbar'
    ],

    # Testing
    tests_require=['tox'],
    cmdclass={'test': Tox},

    # Scripts
    entry_points={
        'console_scripts': [
            'receita = receita.cli:main',
        ],
    },

    # Information
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
