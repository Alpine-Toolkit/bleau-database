####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import os

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read(file_name):

    path = os.path.dirname(__file__)
    if os.path.basename(path) == 'tools':
        path = os.path.dirname(path)
    absolut_file_name = os.path.join(path, file_name)

    return open(absolut_file_name).read()

####################################################################################################

long_description = read('README.rst')

setup_dict = dict(
    name='BleauDataBase',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Bleau Database',
    license = "AGPLv3+",
    keywords = "bleau",
    url='https://github.com/Cosiroc/bleau-database',
    scripts=[],
    packages=['BleauDataBase'],
    data_files = [],
    long_description=long_description,
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Topic :: Other/Nonlisted Topic",
        "Intended Audience :: Other Audience",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        ],
    requires=[
        'ArithmeticInterval'
        'fastkml',
        'geojson',
        'lxml',
        'RTree',
        # Web Application
        'bokeh',
        'flask',
        'flask_wtf',
        'wtforms',
    ],
    )

####################################################################################################
#
# End
#
####################################################################################################
