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

"""This module implements an oriented object database for bouldering areas like Fontainebleau.

Despite the implementation could apply to other areas rather than the area of Fontainebleau, some
attributes are specific to this area like the type of sandstone chaos and the local grade
system.

"""

####################################################################################################

import itertools
import json
import locale
import logging
import math
import re
import urllib.request

####################################################################################################
#
# Non standard modules
#

try:
    import rtree
except ImportError:
    logging.warn('rtree module is not available')
    rtree = None

try:
    import geojson
except ImportError:
    logging.warn('geojson module is not available')
    geojson = None

####################################################################################################

from .FieldObject import InstanceChecker, StringList, FromJsonMixin
from .GeoFormat.GPX import GPX, WayPoint
from .Projection import GeoAngle, GeoCoordinate

####################################################################################################

class PlaceCategory(str):

    """This class defines a category of place."""

    # Fixme: define in the json ?
    __categories__ = ('parking', 'gare', "point d'eau")
    # also: massif, circuit, bloc

    ##############################################

    def __new__(cls, category):

        # Normalise and check
        category = category.lower()
        if category not in cls.__categories__:
            raise ValueError('Unknown category "{}"'.format(category))
        
        return str.__new__(cls, category)

####################################################################################################

class WayNumber:

    """This class defines a way number."""

    __number_re__ = re.compile('^([1-9][0-9]*)(bis|ter|quater)?( ex)?$')
    # tierce

    ##############################################

    def __init__(self, number):

        number = str(number).lower()
        match = self.__number_re__.match(number)
        if match is not None:
            number, variant, ex = match.groups()
            self._number = int(number)
            self._variant = variant
            self._ex = ex
        else:
            raise ValueError('Bad way number "{}"'.format(number))

    ##############################################

    def __str__(self):

        number = str(self._number)
        if self._variant is not None:
            number += self._variant
        if self._ex is not None:
            number += self._ex
        return number

    ##############################################

    @property
    def __json_interface__(self):
        if self._variant is None and self._ex is None:
            return self._number
        else:
            return str(self)

    ##############################################

    def __int__(self):
        return self._number

    ##############################################

    def __float__(self):

        number = float(self._number)
        if self._variant == 'bis':
            number += .1
        elif self._variant == 'ter':
            number += .2
        elif self._variant == 'quater':
            number += .3
        if self._variant == 'ex':
            number += .5
        return number

    ##############################################

    def __lt__(self, other):

        return float(self) < float(other)

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def variant(self):
        return self._variant

    @property
    def ex(self):
        return self._ex

####################################################################################################

class IncompatibleGradeError(Exception):
    pass

class Grade:

    """This class defines a French grade."""

    __grade_re__ = re.compile(r'([1-9])([a-c])?(\+|\-)?')

    ##############################################

    @staticmethod
    def old_grade_iter():

        for major in range(1, 10):
            for minor in ('-', '', '+'):
                yield Grade(str(major) + minor)

    ##############################################

    @staticmethod
    def grade_iter():

        for major in range(1, 10):
            for minor in ('a', 'b', 'c'):
                grade = str(major) + minor
                yield Grade(grade)
                if major >= 6:
                    yield Grade(grade + '+')

    ##############################################

    def __init__(self, grade):

        grade = str(grade).lower()
        match = self.__grade_re__.match(grade)
        if match is not None:
            number, self._letter, self._sign = match.groups()
            self._number = int(number)
            if self._sign == '-' and self._letter is not None:
                raise ValueError('Bad grade "{}" with letter and inf'.format(grade))
            elif self._sign == '+' and self._letter is not None and self._number < 6:
                raise ValueError('Bad grade "{}" with sup < 6'.format(grade))
        else:
            raise ValueError('Bad grade "{}"'.format(grade))

    ##############################################

    def __str__(self):

        grade = str(self._number)
        if self._letter is not None:
            grade += self._letter
        if self._sign is not None:
            grade += self._sign
        return grade

    ##############################################

    @property
    def __json_interface__(self):
        return str(self)

    ##############################################

    def __float__(self):

        value = float(self._number)
        letter = self._letter
        sign = self._sign
        if letter is not None:
            # 6a < 6a+ < 6b < 6b+ < 6c < 6c+
            if letter == 'a':
                value += 1/4
            elif letter == 'b':
                value += 1/2
            else: # c
                value += 3/4
            if sign == "+":
                value += 1/8
        else:
            # Old system: 5 -/inf < 5 < 5 +/sup
            if sign == '-':
                value += 1/4
            elif sign is None:
                value += 1/2
            else:
                value += 3/4
        return value

    ##############################################

    def is_old_grade(self):

        # return ((self._sign is not None and self._letter is None)
        #         or (self._sign is None and self._letter is None))
        # (A.B) + (notA.B) = B
        return self._letter is None

    ##############################################

    @property
    def standard_grade(self):

        if self.is_old_grade():
            sign = self._sign
            grade = str(self._number)
            if sign == '-':
                grade += 'a'
            elif sign is None:
                grade += 'b'
            else:
                grade += 'c'
            return self.__class__(grade)
        else:
            return self

    ##############################################

    def is_incompatible_with(self, other):

        """For exemple the grade 5c+ is incompatible with 5+."""

        # Fixme: versus is_old_grade ?
        if (self._number == other._number
            and (self._sign is not None or other._sign is not None)):
            has_letter1 = self._letter is not None
            has_letter2 = other._letter is not None
            return has_letter1 ^ has_letter2
        else:
            return False

    ##############################################

    def __lt__(self, other):

        # if self.is_incompatible_with(other):
        #     raise IncompatibleGradeError
        # else:
        return float(self) < float(other)

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def letter(self):
        return self._letter

    @property
    def sign(self):
        return self._sign

####################################################################################################

class AlpineGrade:


    """This class defines a French alpin grade."""

    __grade_majors__ = ('EN', 'F', 'PD', 'AD', 'D', 'TD', 'ED', 'EX') # , 'ABO'
    __grade_major_descriptions__ = {
        'EN': 'Enfant',
        'F': 'Facile',
        'PD': 'Peu Difficile', # et non « Pas Difficile » !
        'AD': 'Assez Difficile',
        'D': 'Difficile',
        'TD': 'Très Difficile',
        'ED': 'Extrêmement Difficile',
        'EX': 'Exceptionnellement Difficile',
        # or
        'ABO': 'Abominablement Difficile',
    }
    __grade_major_transcription__ = {
        'EN': None,
        'F': None,
        'PD': '3',
        'AD': '4',
        'D': ('4c', '5b'),
        'TD': ('5c', '6a'),
        'ED': ('6b', '7a'),
        'EX': '7b',
    }
    __grade_minors__ = ('-', '', '+')
    __grades__ = tuple([major + minor
                        for major, minor in
                        itertools.product(__grade_majors__, __grade_minors__)])
    __grade_to_number__ = {grade:i for i, grade in enumerate(__grades__)}

    ##############################################

    @staticmethod
    def grade_iter():

        for grade in AlpineGrade.__grades__:
            yield AlpineGrade(grade)

    ##############################################

    def __init__(self, grade):

        grade = str(grade).upper()
        if grade not in self.__grades__:
            raise ValueError('Bad alpine grade "{}"'.format(grade))

        self._grade = grade
        if grade[-1] in ('-', '+'):
            self._major = grade[:-1]
            self._minor = grade[1]
        else:
            self._major = grade
            self._minor = None

    ##############################################

    def __str__(self):
        return self._grade

    ##############################################

    def __int__(self):
        return self.__grade_to_number__[self._grade]

    ##############################################

    def __float__(self):

        value = self._major
        minor = self._minor
        if minor is None:
            value += 1/2
        elif minor == '-':
            value += 1/4
        else:
            value += 3/4
        
        return value

    ##############################################

    def __lt__(self, other):
        return int(self) < int(other)

    ##############################################

    @property
    def major(self):
        return AlpineGrade(self._major)

    ##############################################

    @property
    def minor(self):
        return self._minor

####################################################################################################

class ChaosType(str):

    """This class defines a type of sandstone chaos."""

    __chaos_types__ = ('A', 'B', 'C', 'D', 'E')
    __chaos_type_descriptions__ = {
        'A': 'Rempart', # Banc de grès
        'B': 'Ouverture des Diaclases',
        'C': 'Chaos vif',
        'D': 'Chaos achevé',
        'E': 'Chaos mort',
    }
    __chaos_type_re__ = re.compile('([A-E])(/([A-E]))?')

    ##############################################

    def __new__(cls, chaos_type):

        chaos_type = chaos_type.upper()
        match = cls.__chaos_type_re__.match(chaos_type)
        if not match:
            raise ValueError('Bad chaos type "{}"'.format(chaos_type))
        # else:
        #     match.groups() # 0 2

        return str.__new__(cls, chaos_type)

####################################################################################################

class Coordinate(FromJsonMixin):

    # Fixme: coordinate versus location ?

    """This class defines a coordinate."""

    latitude = float
    longitude = float

    ##############################################

    def __str__(self):

        return '({0.longitude}, {0.latitude})'.format(self)

    ##############################################

    @property
    def geo_coordinate(self):
        return GeoCoordinate(GeoAngle(self.longitude), GeoAngle(self.latitude))

    @property
    def mercator(self):
        return self.geo_coordinate.mercator

    @property
    def bounding_box(self):
        x, y = self.geo_coordinate.mercator
        return (x, y, x, y)

    ##############################################

    @property
    def __json_interface__(self):
        return self.to_json()

    @property
    def __geo_interface__(self):
        return {'type': 'Point', 'coordinates': (self.longitude, self.latitude)}

####################################################################################################

class WithCoordinate(FromJsonMixin):

    """Base class for :class:`Massif` and :class:`Circuit`."""

    coordinate = None # Fixme: metaclass don't see this attribute

    __gpx_type_prefix__ = 'Bleau/'

    ##############################################

    def __bool__(self):
        return self.coordinate is not None

    ##############################################

    @property
    def pretty_name(self):
        # Fixme: purpose ?
        return str(self)

    ##############################################

    @property
    def gpx_type(self):
        return self.__class__.__name__

    ##############################################

    @property
    def __geo_interface__(self):

        properties = self.to_json(exclude=('coordinate',))
        # Fixme: category
        properties['object'] = self.__class__.__name__
        
        return {'type': 'Feature', 'geometry': self.coordinate, 'properties': properties}

    ##############################################

    @property
    def waypoint(self):

        return WayPoint(name=self.pretty_name,
                        lat=self.coordinate.latitude,
                        lon=self.coordinate.longitude,
                        type=self.__gpx_type_prefix__ + self.gpx_type,
                        # desc=
                        # cmt=
                        # link=
        )

    ##############################################

    def strxfrm(self):

        return locale.strxfrm(str(self))

    ##############################################

    def __lt__(self, other):

        """ Compare name using French collation """

        # return locale.strcoll(str(self), str(other))
        return self.strxfrm() < other.strxfrm()

    ##############################################

    def nearest(self, number_of_items=1, distance_max=None):

        # Fixme: call nearest_massif
        return self.bleau_database.nearest_massif(self, number_of_items, distance_max)

    ##############################################

    def distance_to(self, item):

        x0, y0 = self.coordinate.mercator
        x1, y1 = item.coordinate.mercator
        return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

####################################################################################################

class PlaceBase(WithCoordinate):

    # Fixme: for Boulder, NamedPlace ?

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(**kwargs)
        self.bleau_database = bleau_database

####################################################################################################

class Place(PlaceBase):

    """This class defines a place."""

    coordinate = Coordinate
    name = str

    category = PlaceCategory
    note = str # aka commentaire

    ##############################################

    def __str__(self):
        return self.name

    ##############################################

    @property
    def gpx_type(self):
        return self.category.title()

####################################################################################################

class Massif(PlaceBase):

    """This class defines a « massif »."""

    coordinate = Coordinate
    name = str

    a_pieds = bool # Fixme: fr
    acces = str # Fixme: fr
    alternative_name = str
    chaos_type = ChaosType
    note = str
    parcelles = str # Fixme: fr
    parking = str # Fixme: remove ?
    rdv = str # Fixme: fr
    secteur = str # Fixme: fr, entity ?
    velo = str # Fixme: fr, gare

    # propreté fréquentation exposition débutant

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(bleau_database, **kwargs)
        
        self._circuits = set()

    ##############################################

    def add_circuit(self, circuit):
        self._circuits.add(circuit)

    ##############################################

    @property
    def __json_interface__(self):
        return str(self)

    ##############################################

    def __len__(self):
        return len(self._circuits)

    ##############################################

    def __iter__(self):

        # return iter(sorted(self._circuits, key=lambda x: x.grade))
        # return iter(sorted(self._circuits, key=lambda x: int(x.grade)))
        return iter(sorted(self._circuits))

    ##############################################

    def __str__(self):
        return self.name

    ##############################################

    @property
    def alternative_name_or_name(self):

        # Fixme: purpose ?
        if self.alternative_name:
            return self.alternative_name
        else:
            return self.name

    ##############################################

    @property
    def grades(self):

        return tuple([circuit.grade for circuit in self])

    ##############################################

    @property
    def uniq_grades(self):

        # set lost order
        grades = {circuit.grade for circuit in self._circuits}
        return tuple(sorted(grades))

    ##############################################

    @property
    def major_grades(self):

        grades = {circuit.grade.major for circuit in self._circuits}
        return tuple(sorted(grades))

    ##############################################

    def nearest_point_deau(self, number_of_items=2, distance_max=2000):

        return self.bleau_database.nearest_place(self,
                                                 place_category="point d'eau",
                                                 number_of_items=number_of_items,
                                                 distance_max=distance_max)

####################################################################################################

class BoulderList(list):

    """Factory to check a Boulder list."""

    ##############################################

    def __init__(self, *args):

        super().__init__([Boulder(**kwargs) for kwargs in args])

####################################################################################################

class Boulder(WithCoordinate):

    """This class defines a « boulder »."""

    coordinate = Coordinate
    name = str

    comment = str
    grade = Grade
    number = WayNumber

    ##############################################

    def __lt__(self, other):

        # if self.number is None or self.other is None:
        #     return self.number is None
        # else:
        return self.number < other.number

####################################################################################################

class Circuit(PlaceBase):

    """This class defines a « circuit »."""

    coordinate = Coordinate

    boulders = BoulderList # Fixme: None instead of iter !
    colour = str
    creation_date = int
    gestion = str # Fixme: fr
    grade = AlpineGrade
    massif = InstanceChecker(Massif)
    number = int
    opener = str
    refection_date = int
    status = str
    topos = StringList

    # patiné
    # refection historique

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(bleau_database, **kwargs)
        
        self.massif.add_circuit(self)

    ##############################################

    @property
    def pretty_name(self):
        # Fixme
        return '{0.massif} n°{0.number} {0.grade}'.format(self)

    ##############################################

    @property
    def name(self):
        # -{0.grade}
        return '{0.massif}-{0.number}'.format(self)

    ##############################################

    @property
    def number_of_boulders(self):
        if self.boulders is not None:
            return len(self.boulders)
        else:
            return 0 # None

    ##############################################

    def __str__(self):
        return self.name

    ##############################################

    def __lt__(self, other):

        grade1 = self.grade
        grade2 = other.grade
        if grade1 == grade2:
            return self.number < other.number
        else:
            return grade1 < grade2

    ##############################################

    def has_topo(self):

        return bool(self.topos)

    ##############################################

    def upload_topos(self):

        for url in self.topos:
            if url.endswith('.pdf'):
                # print('Get', url)
                with urllib.request.urlopen(url) as response:
                    document = response.read()
                    pdf_name = url[url.rfind('/')+1:]
                    with open(pdf_name, 'wb') as f:
                        f.write(document)

####################################################################################################

class JsonEncoder(json.JSONEncoder):

    ##############################################

    def default(self, obj):

        if isinstance(obj, Boulder):
            return obj.to_json()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

####################################################################################################

class BleauDataBase:

    """This class represents the database."""

    ##############################################

    def __init__(self, json_file=None, country_code='fr_FR', raise_for_unknown=True):

        # To sort string using French collation
        locale.setlocale(locale.LC_ALL, country_code)
        
        self._items = {}
        self._places = {}
        self._massifs = {}
        self._circuits = {}
        self._number_of_boulders = None
        
        self._rtree_place = None
        self._rtree_massif = None
        self._rtree_circuit = None
        self._ids = {}
        
        if json_file is not None:
            with open(json_file, encoding='utf8') as f:
                # Fixme: object_hook= for Coordinate
                data = json.load(f)
            
            places = [Place(self, raise_for_unknown=raise_for_unknown, **place_dict)
                      for place_dict in data['places']]
            for place in places:
                self.add_place(place)

            massifs = [Massif(self, raise_for_unknown=raise_for_unknown, **massif_dict)
                       for massif_dict in data['massifs']]
            for massif in massifs:
                self.add_massif(massif)
            
            for circuit_dict in data['circuits']:
                circuit_dict['massif'] = self._massifs[circuit_dict['massif']]
                # Fixme: circuit -> massif -> bleau_database
                self.add_circuit(Circuit(self, raise_for_unknown=raise_for_unknown, **circuit_dict))

    ##############################################

    # def __del__(self):

    #     del self._rtree

    ##############################################

    @property
    def number_of_circuits(self):
        return len(self._circuits)

    @property
    def number_of_circuits_with_topos(self):
        return len([circuit for circuit in self.circuits
                    if circuit.has_topo()])

    @property
    def number_of_massifs(self):
        return len(self._massifs)

    @property
    def number_of_boulders(self):
        if self._number_of_boulders is None:
            self._number_of_boulders = sum([circuit.number_of_boulders for circuit in self.circuits])
        return self._number_of_boulders

    @property
    def places(self):
        return iter(sorted(self._places.values()))

    @property
    def massifs(self):
        return iter(sorted(self._massifs.values()))

    @property
    def circuits(self):
        # Circuit.__lt__ sort by grade
        return iter(sorted(self._circuits.values(), key=lambda circuit: circuit.strxfrm()))

    @property
    def secteurs(self):
        # Fixme: in case of misspelling ?
        # Fixme: unsorted massif iter
        return sorted({massif.secteur for massif in self._massifs.values()})
                      # if massif.secteur is not None

    ##############################################

    def __contains__(self, key):

        return key in self._items

    ##############################################

    def __getitem__(self, key):

        return self._items[key]

    ##############################################

    def _add_item(self, dictionary, item):

        name = str(item)
        if name not in self._items:
            self._items[name] = item
            dictionary[name] = item
        else:
            raise KeyError('Name is already registered: "{}"'.format(name))

    ##############################################

    def add_place(self, place):

        self._add_item(self._places, place)

    ##############################################

    def add_massif(self, massif):

        self._add_item(self._massifs, massif)

    ##############################################

    def add_circuit(self, circuit):

        self._add_item(self._circuits, circuit)

    ##############################################

    def to_json(self, json_file=None):

        data = {
            'places': [place.to_json() for place in self.places],
            'massifs': [massif.to_json() for massif in self.massifs],
            'circuits': [circuit.to_json() for circuit in self.circuits],
        }

        kwargs = dict(cls=JsonEncoder, indent=2, ensure_ascii=False, sort_keys=True)
        if json_file is not None:
            with open(json_file, 'w', encoding='utf8') as f:
                json.dump(data, f, **kwargs)
        else:
            return json.dumps(data, **kwargs)

    ##############################################

    def to_geojson(self, json_path=None, places=True, massifs=True, circuits=True):

        features = []
        if places:
            features.extend([place for place in self.places if place])
        if massifs:
            features.extend([massif for massif in self.massifs if massif])
        if circuits:
            # Fixme: boulders
            features.extend([circuit for circuit in self.circuits if circuit])
        feature_collections = geojson.FeatureCollection(features)
        if not geojson.is_valid(feature_collections):
            raise ValueError('Non valid GeoJSON')
        # Fixme: crs geojson.named API
        
        kwargs = dict(indent=2, ensure_ascii=False, sort_keys=True)
        if json_path is not None:
            with open(json_path, 'w', encoding='utf8') as f:
                geojson.dump(feature_collections, f, **kwargs)
        else:
            return geojson.dumps(feature_collections, **kwargs)

    ##############################################

    def to_gpx(self, gpx_path=None, places=True, massifs=True, circuits=True):

        # gpx_schema = 'doc/geo-formats/gpx/gpx-v1.1.xsd'
        # gpx_schema = None

        gpx = GPX()
        if places:
            gpx.add_waypoints([place.waypoint for place in self.places if place])
        if massifs:
            gpx.add_waypoints([massif.waypoint for massif in self.massifs if massif])
        if circuits:
            gpx.add_waypoints([circuit.waypoint for circuit in self.circuits if circuit])
        if gpx_path is not None:
            gpx.write(gpx_path)
        else:
            return gpx

    ##############################################

    def _build_rtree(self, items):

        if rtree is None:
            raise NotImplementedError
        
        rtree_ = rtree.index.Index()
        for item in items:
            if item:
                rtree_.insert(id(item), item.coordinate.bounding_box)
                self._ids[id(item)] = item
        return rtree_

    ##############################################

    @property
    def rtree_place(self):

        if self._rtree_place is None:
            self._rtree_place = self._build_rtree(self.places)
        return self._rtree_place

    ##############################################

    @property
    def rtree_massif(self):

        if self._rtree_massif is None:
            self._rtree_massif = self._build_rtree(self.massifs)
        return self._rtree_massif

    ##############################################

    @property
    def rtree_circuit(self):

        if self._rtree_circuit is None:
            self._rtree_circuit = self._build_rtree(self.circuits)
        return self._rtree_circuit

    ##############################################

    def _nearest(self, rtree_, item, number_of_items=1, distance_max=None):

        number_of_items += 1
        # Fixme: segfault ???
        # return [x.object for x in rtree.nearest(item.coordinate.bounding_box, number_of_items, objects=True)]
        items = [self._ids[x] for x in rtree_.nearest(item.coordinate.bounding_box, number_of_items)]
        items = [x for x in items if x is not item]
        if distance_max is not None:
            items = [x for x in items if item.distance_to(x) <= distance_max]
        return items

    ##############################################

    def nearest_massif(self, item, number_of_items=1, distance_max=None):

        return self._nearest(self.rtree_massif, item, number_of_items, distance_max)

    ##############################################

    def nearest_place(self, item, place_category, number_of_items=1, distance_max=None):

        places = self._nearest(self.rtree_place, item, number_of_items=1000, distance_max=distance_max)
        places = [place for place in places if place.category == place_category]
        
        return places[:number_of_items]

    ##############################################

    def nearest_circuit(self, item, number_of_items=1, distance_max=None):

        return self._nearest(self.rtree_circuit, item, number_of_items, distance_max)

    ##############################################

    def filter_by(self,
                  a_pieds=None,
                  secteurs=None,
                  chaos_type=None,
                  grades=None,
                  major_grades=None,
    ):

        # print(a_pieds, secteurs, chaos_type, grades, major_grades)
        massifs = self.massifs
        if a_pieds is not None:
            massifs = [massif for massif in massifs if massif.a_pieds]
        if secteurs is not None:
            # massif.secteur and
            massifs = [massif for massif in massifs if massif.secteur in secteurs]
        if chaos_type is not None:
            # Fixme: in ?
            chaos_type = set(chaos_type)
            massifs = [massif for massif in massifs
                       if massif.chaos_type and set(massif.chaos_type.split('/')) >= chaos_type]
        if grades is not None or major_grades is not None:
            if grades is not None:
                grades = set(grades)
                massifs = [massif for massif in massifs if set(massif.uniq_grades) >= grades]
            else:
                grades = set(major_grades)
                massifs = [massif for massif in massifs if set(massif.major_grades) >= grades]
        # print(massifs)

        return massifs

####################################################################################################
#
# End
#
####################################################################################################
