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
    # import pykml
    from pykml import parser as kml_parser
    from lxml import etree
except ImportError:
    kml_parser = None

####################################################################################################

from ..BleauDataBase import Place

####################################################################################################

def import_kml_file(kml_path):

    with open(kml_path) as f:
        doc = kml_parser.parse(f)
    
    folder = doc.getroot().Folder # .Document.Folder
    
    places = []
    for placemark in folder.iterchildren():
        if etree.QName(placemark.tag).localname == 'Placemark':
            if hasattr(placemark, 'Point'):
                latitude, longitude = [float(x) for x in str(placemark.Point.coordinates).split(',')]
                coordinate = dict(longitude=longitude, latitude=latitude)
            else:
                raise ValueError('Missing point coordinate')
            if hasattr(placemark, 'name'):
                name = placemark.name
            else:
                raise ValueError('Missing name')
            if hasattr(placemark, 'description'):
                description = placemark.description
            else:
                description = None
            place = Place(coordonne=coordinate, nom=name, notes=description, bleau_database=None)
            places.append(place)
    
    return places

####################################################################################################
#
# End
#
####################################################################################################
