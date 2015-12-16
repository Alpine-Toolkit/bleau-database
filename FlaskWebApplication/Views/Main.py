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

from flask import current_app, Blueprint, render_template, request

# from wtforms import Form
from flask_wtf import Form
from wtforms import BooleanField, TextField, SelectMultipleField, SubmitField
# from wtforms import validators

from BleauDataBase.BleauDataBase import AlpineGrade, Coordinate

####################################################################################################

from ..Model import model

####################################################################################################

main = Blueprint('main', __name__, url_prefix='/main')

@main.route('/')
def index():
    return render_template('main.html', bleau_database=model.bleau_database)

@main.route('/a-propos')
def a_propos():
    return render_template('a-propos.html')

@main.route('/data')
def data():
    return render_template('data.html')

@main.route('/massifs')
def massifs():
    return render_template('massifs.html', massifs=model.bleau_database.massifs)

@main.route('/massifs-par-secteur')
def massifs_par_secteur():
    return render_template('massifs-par-secteur.html', bleau_database=model.bleau_database)

@main.route('/place/<place>')
def place(place):
    place = model.bleau_database[place]
    return render_template('place.html', place=place)

@main.route('/massif/<massif>')
def massif(massif):
    massif = model.bleau_database[massif]
    circuit_statistics = model.circuit_statistics_cache[[circuit for circuit in massif]]
    return render_template('massif.html',
                           massif=massif, place=massif,
                           circuit_statistics=circuit_statistics)

@main.route('/circuit/<circuit>')
def circuit(circuit):
    circuit = model.bleau_database[circuit]
    circuit_statistics = model.circuit_statistics_cache[[circuit]]
    return render_template('circuit.html',
                           massif=circuit.massif, circuit=circuit,
                           place=circuit,
                           circuit_statistics=circuit_statistics)

@main.route('/geoportail')
def geoportail():
    extent = model.bleau_database.mercator_area_interval.enlarge(1000)
    return render_template('geoportail-map.html', extent=extent,
                           massif=None, place=None)

@main.route('/geoportail/<massif>')
def geoportail_massif(massif):
    massif = model.bleau_database[massif]
    return render_template('geoportail-map.html', massif=massif, place=massif)

@main.route('/google-map/<massif>')
def google_map(massif):
    massif = model.bleau_database[massif]
    return render_template('google-map.html', massif=massif, place=massif)

####################################################################################################

class MassifSearchForm(Form):
    a_pieds = BooleanField('À pieds')
    secteurs = SelectMultipleField('Secteurs',
                                   choices=[(secteur, secteur)
                                            for secteur in model.bleau_database.secteurs])
    chaos_type = SelectMultipleField('Type de chaos',
                                     choices=[(x, x) for x in ('A', 'B', 'C', 'D', 'E')])
    # cotation = TextField('Cotation')
    grades = SelectMultipleField('Cotations',
                                 choices=[(x, x) for x in AlpineGrade.__grade_majors__ if x != 'EX'])

@main.route('/search-massifs', methods=['GET', 'POST'])
def search_massifs():
    form = MassifSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        a_pieds = form.a_pieds.data
        secteurs = form.secteurs.data
        chaos_type = form.chaos_type.data
        grades = form.grades.data
        # grades = form.grade.data.strip()
        # grades = {grade.upper() for grade in grades.split(' ') if grade}
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        kwargs = {}
        if a_pieds:
            kwargs['a_pieds'] = a_pieds
        if secteurs:
            kwargs['secteurs'] = secteurs
        if chaos_type:
            kwargs['chaos_type'] = chaos_type
        if grades:
            kwargs['major_grades'] = grades
        massifs = model.bleau_database.filter_by(**kwargs)
        return render_template('search-massifs.html', form=form, massifs=massifs)
    return render_template('search-massifs.html', form=form, massifs=[])

####################################################################################################
#
# End
#
####################################################################################################
