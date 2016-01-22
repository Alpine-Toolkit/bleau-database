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

from functools import wraps
import os

from flask import Flask, g, request, render_template, abort, url_for
from flask.ext.cache import Cache
from flask.ext.babel import Babel
from flask_sitemap import Sitemap, sitemap_page_needed

####################################################################################################

from .config import LANGUAGES
from .Singleton import SingletonMetaClass

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
            # return abort(404)
            return 'fr'
    else:
        # otherwise try to guess the language from the user accept header the browser transmits.
        # The best match wins.
        return request.accept_languages.best_match(LANGUAGES.keys())

####################################################################################################

# @sitemap_page_needed.connect
# def create_page(app, page, urlset):
#     # Fixme: never called and sitemap is undefined
#     # print('create_page')
#     cache[page] = sitemap.render_page(urlset=urlset)

def load_page(fn):
    @wraps(fn)
    def loader(*args, **kwargs):
        page = kwargs.get('page')
        cache = FlaskWebApplicationSingleton().cache
        data = cache.get(page)
        return data if data else fn(*args, **kwargs)
    return loader

####################################################################################################

class FlaskWebApplicationSingleton(metaclass=SingletonMetaClass):

    """Singleton used to pass global"""

    # Fixme: better design ???

    application = None
    cache = None
    babel = None
    sitemap = None

####################################################################################################

class FlaskWebApplication:

    ##############################################

    def __init__(self, config_path, bleau_database, server_name=None):

        self.application = Flask(__name__)
        self.application.logger.info("Start Bleau Database Web Application")
        
        self.application.config.from_pyfile(config_path)
        # Fixme: right way?
        self.application.config['bleau_database'] = bleau_database
        
        self.application.secret_key = os.urandom(24)
        # WTF_CSRF_SECRET_KEY =
        
        self.cache = Cache(self.application, config={'CACHE_TYPE': 'simple'})
        
        self.babel = Babel(self.application)
        self.babel.localeselector(get_locale)
        
        self.application.error_handler_spec[None][404] = page_not_found
        
        if server_name is not None:
            self.application.config['SERVER_NAME'] = server_name
        # self.app.config['SITEMAP_GZIP'] = True
        self.application.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
        self.application.config['SITEMAP_VIEW_DECORATORS'] = [load_page]
        self.sitemap = Sitemap(app=self.application)
        
        from .Model import model
        model.init_app(self.application)
        
        application_singleton = FlaskWebApplicationSingleton()
        application_singleton.application = self.application
        application_singleton.cache = self.cache
        application_singleton.babel = self.babel
        application_singleton.sitemap = self.sitemap
        
        from .Views.Main import main
        self.application.register_blueprint(main)
        
        # Map / to /fr
        # Fixme: /foo redirect to main instead of 404
        self.application.add_url_rule('/', 'main.index')

    ##############################################

    def run(self):
        self.application.run()

####################################################################################################
#
# End
#
####################################################################################################
