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

import logging

try:
    from lxml import etree
except ImportError:
    logging.warn('lxml module is not available')
    etree = None

####################################################################################################

from ..FieldObject import FromJsonMixin

####################################################################################################

class WayPoint(FromJsonMixin):

    # < wpt lat="latitudeType [1] ?" lon="longitudeType [1] ?">
    #   <ele> xsd:decimal </ele> [0..1] ?
    #   <time> xsd:dateTime </time> [0..1] ?
    #   <magvar> degreesType </magvar> [0..1] ?
    #   <geoidheight> xsd:decimal </geoidheight> [0..1] ?
    #   <name> xsd:string </name> [0..1] ?
    #   <cmt> xsd:string </cmt> [0..1] ?
    #   <desc> xsd:string </desc> [0..1] ?
    #   <src> xsd:string </src> [0..1] ?
    #   <link> linkType </link> [0..*] ?
    #   <sym> xsd:string </sym> [0..1] ?
    #   <type> xsd:string </type> [0..1] ?
    #   <fix> fixType </fix> [0..1] ?
    #   <sat> xsd:nonNegativeInteger </sat> [0..1] ?
    #   <hdop> xsd:decimal </hdop> [0..1] ?
    #   <vdop> xsd:decimal </vdop> [0..1] ?
    #   <pdop> xsd:decimal </pdop> [0..1] ?
    #   <ageofdgpsdata> xsd:decimal </ageofdgpsdata> [0..1] ?
    #   <dgpsid> dgpsStationType </dgpsid> [0..1] ?
    #   <extensions> extensionsType </extensions> [0..1] ?
    # </wpt>

    lat = float
    lon = float
    ele = float
    time = str
    magvar = float
    geoidheight = float
    name = str
    cmt = str
    desc = str
    src = str
    link = str
    sym = str
    type = str
    fix = str
    sat = int
    hdop = float
    vdop = float
    pdop = float
    ageofdgpsdata = float
    dgpsid = int

####################################################################################################

class GPX:

    ##############################################

    def __init__(self, gpx_path=None, schema_path=None):

        self._waypoints = []
        
        if gpx_path is not None:
            self._parse(gpx_path, schema_path)

    ##############################################

    def _parse(self, gpx_path, schema_path=None):

        if schema_path is not None:
            schema = etree.XMLSchema(file=schema_path)
            parser = etree.XMLParser(schema=schema)
        else:
            parser = None
        
        namespaces = dict(topografix='http://www.topografix.com/GPX/1/1')
        
        tree = etree.parse(gpx_path, parser=parser)
        
        # root = tree.getroot()
        # for item in root:
        #    print(item.tag, tree.getpath(item))
        
        waypoints = []
        for waypoint_element in tree.xpath('topografix:wpt', namespaces=namespaces):
            d = self._attribute_to_dict(waypoint_element, ('lat', 'lon'))
            for element in waypoint_element:
                field = etree.QName(element.tag).localname
                d[field] = element.text
            waypoint = WayPoint(**d)
            waypoints.append(waypoint)
        self._waypoints = waypoints

    ##############################################

    @staticmethod
    def _attribute_to_dict(node, fields):

        attributes = node.attrib
        return {field:attributes[field] for field in fields}

    ##############################################

    @property
    def waypoints(self):
        return self._waypoints

    ##############################################

    def add_waypoint(self, waypoint):
        self._waypoints.append(waypoint)

    ##############################################

    def add_waypoints(self, waypoints):
        self._waypoints.extend(waypoints)

    ##############################################

    def add_new_waypoint(self, **kwargs):
        self.append_waypoint(WayPoint(**kwargs))

    ##############################################

    def write(self, path, encoding='utf-8'):

        with etree.xmlfile(path,
                           encoding=encoding,
                           compression=None,
                           close=True,
                           buffered=True) as xf:
            xf.write_declaration() # standalone=True
            attributes = {
                'version': '1.1',
                'creator': 'BleauDataBase',
                'xmlns': 'http://www.topografix.com/GPX/1/1',
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
            }
            with xf.element('gpx', **attributes):
                for waypoint in self._waypoints:
                    d = waypoint.to_json(only_defined=True)
                    attributes = {field:str(d[field]) for field in ('lon', 'lat')}
                    del d['lon']
                    del d['lat']
                    with xf.element('wpt', **attributes):
                        # Fixme: iter ?
                        # for field in waypoint.__field_names__:
                        #     value = getattr(waypoint, field)
                        #     if value is not None:
                        for field, value in d.items():
                            with xf.element(field):
                                xf.write(str(value))
            xf.flush()

####################################################################################################
#
# End
#
####################################################################################################
