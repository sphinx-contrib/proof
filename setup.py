# Copyright 2015 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Installer"""

from setuptools import setup, find_packages
import codecs
import os

def readme():
    directory = os.path.dirname(os.path.join(
        os.getcwd(),
        __file__,
        ))
    with codecs.open(
        os.path.join(directory, "README.rst"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()

setup(
        name='sphinxcontrib-proof',
        version="0.1.0",
        packages=find_packages(exclude=["test*"]),
        setup_requires=["hgtools"],
        install_requires=[
            "sphinx",
            ],
        include_package_data=True,
        author='Louis Paternault',
        author_email='spalax@gresille.org',
        description="This packages contains the Proof sphinx extension, which provides directives to typeset theorems, lemmas, proofs, etc.",
        url='https://git.framasoft.org/spalax/sphinxcontrib-proof',
        license="AGPLv3 or any later version",
        #test_suite="test.suite",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Framework :: Sphinx :: Extension",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            "Operating System :: Unix",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Topic :: Documentation :: Sphinx",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        long_description=readme(),
        zip_safe = False,
)
