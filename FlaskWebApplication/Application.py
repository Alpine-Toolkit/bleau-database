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

from flask import Flask, g, request, render_template, abort
from flask.ext.babel import Babel

####################################################################################################

from .config import LANGUAGES

####################################################################################################

# @app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found-404.html'), 404

####################################################################################################

# @babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     return user.locale
    lang_code = getattr(g, 'lang_code', None)
    if lang_code is not None:
        if lang_code in LANGUAGES.keys():
            return lang_code
        else:
            return abort(404)
    else:
        # otherwise try to guess the language from the user accept header the browser transmits.
        # The best match wins.
        return request.accept_languages.best_match(LANGUAGES.keys())

####################################################################################################

def create_application(config_path, bleau_database):

    application = Flask(__name__)
    application.logger.info("Start Bleau Database Web Application")
    
    application.config.from_pyfile(config_path)
    # Fixme: right way?
    application.config['bleau_database'] = bleau_database
    application.error_handler_spec[None][404] = page_not_found
    babel = Babel(application)
    babel.localeselector(get_locale)
    
    from .Model import model
    model.init_app(application)
    
    from .Views.Main import main
    application.register_blueprint(main)
    
    # Map / to /fr
    application.add_url_rule('/', 'main.index')
    
    application.secret_key = os.urandom(24)
    # WTF_CSRF_SECRET_KEY =
    
    return application, babel

####################################################################################################
#
# End
#
####################################################################################################
