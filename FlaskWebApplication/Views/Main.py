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

from flask import Blueprint, render_template, request, g, url_for, send_from_directory
from flask_babel import lazy_gettext

# from wtforms import Form
from flask_wtf import Form
from wtforms import BooleanField, TextField, SelectMultipleField, SubmitField
# from wtforms import validators

####################################################################################################

from BleauDataBase.BleauDataBase import AlpineGrade, Coordinate

from ..config import LANGUAGES
from ..Model import model

from ..Application import FlaskWebApplicationSingleton
application_singleton = FlaskWebApplicationSingleton()
application = application_singleton.application
cache = application_singleton.cache
sitemap = application_singleton.sitemap

####################################################################################################

main = Blueprint('main', __name__, url_prefix='/<lang_code>')

@main.url_defaults
def add_language_code(endpoint, values):
    # Fixme: purpose ?
    # print('add_language_code', endpoint, values)
    try:
        values.setdefault('lang_code', g.lang_code)
    except AttributeError:
        # Fixme: ???
        values.setdefault('lang_code', 'fr')

@main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    # print('pull_lang_code', endpoint, values)
    g.lang_code = values.pop('lang_code', 'fr')

def render_template_i18n(template, **kwgars):
    page_path = request.path[4:] # /fr/
    return render_template(template,
                           lang_code=g.lang_code,
                           page_path=page_path,
                           **kwgars)

####################################################################################################

@sitemap.register_generator
def sitemap():

    bleau_database=model.bleau_database
    for lang_code in LANGUAGES.keys():
        kwarg = dict(lang_code=lang_code, _external=True)
        for page in (
                'a_propos',
                'contribute',
                'data',
                'environment',
                'fontainebleau',
                'geoportail',
                'information', # ...
                'massifs',
                'massifs_by_secteur',
                'mentions_legales',
                'search_massifs',
                ):
            yield url_for('main.' + page, **kwarg)
        for place in bleau_database.places:
            yield url_for('main.place', place=str(place), **kwarg)
        for massif in bleau_database.massifs:
            yield url_for('main.massif', massif=str(massif), **kwarg)
        for circuit in bleau_database.circuits:
            yield url_for('main.circuit', circuit=str(circuit), **kwarg)
        # persons ...

        # '/geoportail/<massif>'
        # '/google-map/<massif>'

####################################################################################################

@application.route('/robots.txt')
def static_from_root():
    return send_from_directory(application.static_folder, request.path[1:])

@cache.cached()
@main.route('/')
def index():
    return render_template_i18n('main.html', bleau_database=model.bleau_database)

@cache.cached()
@main.route('/mentions-legales')
def mentions_legales():
    return render_template_i18n('mentions-legales.html')

@cache.cached()
@main.route('/a-propos')
def a_propos():
    return render_template_i18n('a-propos.html', bleau_database=model.bleau_database)

@cache.cached()
@main.route('/fontainebleau')
def fontainebleau():
    return render_template_i18n('fontainebleau.html')

@cache.cached()
@main.route('/environment')
def environment():
    return render_template_i18n('environment.html')

@cache.cached()
@main.route('/contribute')
def contribute():
    return render_template_i18n('contribute.html')

@cache.cached()
@main.route('/data')
def data():
    return render_template_i18n('data.html')

@cache.cached()
@main.route('/information')
def information():
    return render_template_i18n('information/information.html')

@cache.cached()
@main.route('/information/statistics')
def statistics():
    circuits = model.bleau_database.circuits
    circuit_statistics = model.circuit_statistics_cache[list(circuits)]
    return render_template_i18n('information/statistics.html',
                                circuit_statistics=circuit_statistics)

@cache.cached()
@main.route('/information/places')
def places():
    return render_template_i18n('information/places.html',
                                places=list(model.bleau_database.places))

@cache.cached()
@main.route('/information/affiliations')
def affiliations():
    return render_template_i18n('information/affiliations.html',
                                affiliations=model.bleau_database.affiliations)

@cache.cached()
@main.route('/information/openers')
def openers():
    return render_template_i18n('information/openers.html',
                                persons=model.bleau_database.persons)

@cache.cached()
@main.route('/information/maintainers')
def maintainers():
    return render_template_i18n('information/maintainers.html',
                                persons=model.bleau_database.persons)
@cache.cached()
@main.route('/information/person/<person>')
def person(person):
    person = model.bleau_database.persons[person]
    return render_template_i18n('information/person.html',
                                person=person)

@cache.cached()
@main.route('/information/missing')
def missing_information():
    return render_template_i18n('information/missing.html',
                                massifs=list(model.bleau_database.massifs)) # Fixme: iter run once

@cache.cached()
@main.route('/massifs')
def massifs():
    return render_template_i18n('massifs.html', massifs=model.bleau_database.massifs)

# Fixme: Fr
@cache.cached()
@main.route('/massifs-by-secteur')
def massifs_by_secteur():
    return render_template_i18n('massifs-par-secteur.html', bleau_database=model.bleau_database)

@cache.cached()
@main.route('/place/<place>')
def place(place):
    place = model.bleau_database[place]
    return render_template_i18n('place.html', place=place)

@cache.cached()
@main.route('/massif/<massif>')
def massif(massif):
    massif = model.bleau_database[massif]
    circuit_statistics = model.circuit_statistics_cache[[circuit for circuit in massif]]
    return render_template_i18n('massif.html',
                                massif=massif, place=massif,
                                circuit_statistics=circuit_statistics)

@cache.cached()
@main.route('/circuit/<circuit>')
def circuit(circuit):
    circuit = model.bleau_database[circuit]
    circuit_statistics = model.circuit_statistics_cache[[circuit]]
    return render_template_i18n('circuit.html',
                                massif=circuit.massif, circuit=circuit,
                                place=circuit,
                                circuit_statistics=circuit_statistics)

@cache.cached()
@main.route('/geoportail')
def geoportail():
    extent = model.bleau_database.mercator_area_interval.enlarge(1000)
    return render_template_i18n('geoportail-map.html', extent=extent,
                                massif=None, place=None)

@cache.cached()
@main.route('/geoportail/<massif>')
def geoportail_massif(massif):
    massif = model.bleau_database[massif]
    return render_template_i18n('geoportail-map.html', massif=massif, place=massif)

@cache.cached()
@main.route('/google-map/<massif>')
def google_map(massif):
    massif = model.bleau_database[massif]
    return render_template_i18n('google-map.html', massif=massif, place=massif)

####################################################################################################

class MassifSearchForm(Form):
    on_foot = BooleanField(lazy_gettext('À pieds'))
    secteurs = SelectMultipleField(lazy_gettext('Secteurs'),
                                   choices=[(secteur, secteur)
                                            for secteur in model.bleau_database.secteurs])
    chaos_type = SelectMultipleField(lazy_gettext('Type de chaos'),
                                     choices=[(x, x) for x in ('A', 'B', 'C', 'D', 'E')])
    # cotation = TextField('Cotation')
    grades = SelectMultipleField(lazy_gettext('Cotations'),
                                 choices=[(x, x) for x in AlpineGrade.__grade_majors__ if x != 'EX'])

# @cache.cached()
@main.route('/search-massifs', methods=['GET', 'POST'])
def search_massifs():
    form = MassifSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        on_foot = form.on_foot.data
        secteurs = form.secteurs.data
        chaos_type = form.chaos_type.data
        grades = form.grades.data
        # grades = form.grade.data.strip()
        # grades = {grade.upper() for grade in grades.split(' ') if grade}
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        kwargs = {}
        if on_foot:
            kwargs['on_foot'] = on_foot
        if secteurs:
            kwargs['secteurs'] = secteurs
        if chaos_type:
            kwargs['chaos_type'] = chaos_type
        if grades:
            kwargs['major_grades'] = grades
        massifs = model.bleau_database.filter_by(**kwargs)
        return render_template_i18n('search-massifs.html', form=form, massifs=massifs)
    return render_template_i18n('search-massifs.html', form=form, massifs=[])

####################################################################################################
#
# End
#
####################################################################################################
