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

try:
    import fastkml
except ImportError:
    fastkml = None

####################################################################################################

from ..BleauDataBase import Place

####################################################################################################

def import_kml_file(kml_path):

    with open(kml_path) as f:
        doc = f.read()

    kml_document = fastkml.kml.KML()
    kml_document.from_string(doc)

    places = []
    for folder in kml_document.features():
        for placemark in folder.features():
            coordinate = dict(longitude=placemark.geometry.x, latitude=placemark.geometry.y)
            place = Place(coordinate=coordinate, name=placemark.name, note=placemark.description,
                          bleau_database=None)
            places.append(place)

    return places

####################################################################################################
#
# End
#
####################################################################################################
