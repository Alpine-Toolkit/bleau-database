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

from flask import Flask, g, request
from flask.ext.babel import Babel

####################################################################################################

# @babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     return user.locale
    # otherwise try to guess the language from the user accept header the browser transmits.
    # The best match wins.
    locale = request.accept_languages.best_match(['fr', 'en'])
    print('LOCALE', locale)
    return locale

####################################################################################################

def create_application(config_path, bleau_database):

    application = Flask(__name__)
    
    application.config.from_pyfile(config_path)
    # Fixme: right way?
    application.config['bleau_database'] = bleau_database
    babel = Babel(application)
    babel.localeselector(get_locale)
    
    from .Model import model
    model.init_app(application)
    
    from .Views.Main import main, index
    application.register_blueprint(main)
    application.add_url_rule('/', 'main.index')
    
    application.secret_key = os.urandom(24)
    # WTF_CSRF_SECRET_KEY =
    
    return application, babel

####################################################################################################
#
# End
#
####################################################################################################
