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

# activate_this = '/path/to/env/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))

####################################################################################################

import os

from BleauDataBase.BleauDataBase import BleauDataBase
from FlaskWebApplication.Application import create_application

####################################################################################################

json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'bleau.json')
bleau_database = BleauDataBase(json_file)

# Fixme: if DEBUG = True then reload ...
# config_path = os.path.join(os.path.dirname(__file__), 'config.py')
config_path = 'config.py'
application, babel = create_application(config_path, bleau_database)

from flask import redirect, url_for

# @application.route('/')
# def rootindex():
#     redirect(url_for('/main'))

####################################################################################################
#
# End
#
####################################################################################################
