####################################################################################################
#
# Bleau Database
# Copyright (C) 2015 Fabrice Salvaire
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
#
####################################################################################################

####################################################################################################

from flask import current_app, Blueprint, render_template, request

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
#
# End
#
####################################################################################################
