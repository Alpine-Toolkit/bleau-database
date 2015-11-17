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

from BleauDataBase.BleauDataBase import Cotation

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

@main.route('/massifs')
def massifs():
    return render_template('massifs.html', massifs=model.bleau_database.massifs)

@main.route('/massifs-par-secteur')
def massifs_par_secteur():
    return render_template('massifs-par-secteur.html', bleau_database=model.bleau_database)

@main.route('/massif/<massif>')
def massif(massif):
    massif = model.bleau_database[massif]
    return render_template('massif.html', massif=massif)

@main.route('/geoportail/<massif>')
def geoportail(massif):
    massif = model.bleau_database[massif]
    return render_template('geoportail-map.html', massif=massif)

@main.route('/google-map/<massif>')
def google_map(massif):
    massif = model.bleau_database[massif]
    return render_template('google-map.html', massif=massif)

####################################################################################################

class MassifSearchForm(Form):
    a_pieds = BooleanField('À pieds')
    secteurs = SelectMultipleField('Secteurs',
                                   choices=[(secteur, secteur)
                                            for secteur in model.bleau_database.secteurs])
    type_de_chaos = SelectMultipleField('Type de chaos',
                                        choices=[(x, x) for x in ('A', 'B', 'C', 'D', 'E')])
    # cotation = TextField('Cotation')
    cotations = SelectMultipleField('Cotations',
                                    choices=[(x, x) for x in Cotation.__cotation_majors__])

@main.route('/search-massifs', methods=['GET', 'POST'])
def search_massifs():
    form = MassifSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        a_pieds = form.a_pieds.data
        secteurs = form.secteurs.data
        type_de_chaos = form.type_de_chaos.data
        cotations = form.cotations.data
        # cotations = form.cotation.data.strip()
        # cotations = {cotation.upper() for cotation in cotations.split(' ') if cotation}
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        kwargs = {}
        if a_pieds:
            kwargs['a_pieds'] = a_pieds
        if secteurs:
            kwargs['secteurs'] = secteurs
        if type_de_chaos:
            kwargs['type_de_chaos'] = type_de_chaos
        if cotations:
            kwargs['major_cotations'] = cotations
        massifs = model.bleau_database.filter_by(**kwargs)
        return render_template('search-massifs.html', form=form, massifs=massifs)
    return render_template('search-massifs.html', form=form, massifs=[])

####################################################################################################
#
# End
#
####################################################################################################