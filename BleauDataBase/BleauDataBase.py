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

# Fixme: français -> english ?

####################################################################################################

import itertools
import json
import locale
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
    rtree = None

try:
    import geojson
except ImportError:
    geojson = None

####################################################################################################

from .Projection import GeoAngle, GeoCoordinate

####################################################################################################

class Field:

    """This class defines a field by its name and factory."""

    ##############################################

    def __init__(self, name, factory):

        self.name = name
        self.factory = factory

####################################################################################################

class InstanceChecker:

    """Factory to check the type of an instance object."""

    ##############################################

    def __init__(self, cls):

        self._cls = cls

    ##############################################

    def __call__(self, obj):

        if isinstance(obj, self._cls):
            return obj
        else:
            raise ValueError

####################################################################################################

class StringList(list):

    """Factory to check a string list."""

    ##############################################

    def __init__(self, *args):

        super().__init__([str(x) for x in args])

####################################################################################################

class PlaceType(str):

    """This class defines a type of place."""

    __types__ = ('parking', 'gare', "point d'eau")

    ##############################################

    def __new__(cls, type_de_place):

        type_de_place = type_de_place.lower()
        if type_de_place not in cls.__types__:
            raise ValueError
        
        return str.__new__(cls, type_de_place)

####################################################################################################

class Cotation(str):

    """This class defines a circuit grade."""

    __cotation_majors__ = ('EN', 'F', 'PD', 'AD', 'D', 'TD', 'ED')
    __cotation_major_descriptions__ = {
        'EN': 'Enfant',
        'F': 'Facile',
        'PD': 'Peu Difficile',
        'AD': 'Assez Difficile',
        'D': 'Difficile',
        'TD': 'Très Difficile',
        'ED': 'Extrêmement Difficile',
    }
    __cotation_minors__ = ('-', '', '+')
    __cotations__ = tuple([major + minor
                           for major, minor in
                           itertools.product(__cotation_majors__, __cotation_minors__)])
    __cotation_to_number__ = {cotation:i for i, cotation in enumerate(__cotations__)}

    ##############################################

    def __new__(cls, cotation):

        cotation = cotation.upper()
        if cotation not in cls.__cotations__:
            raise ValueError
        
        return str.__new__(cls, cotation)

    ##############################################

    def __int__(self):
        return self.__cotation_to_number__[self]

    ##############################################

    def __lt__(self, other):
        return int(self) < int(other)

    ##############################################

    @property
    def major(self):

        # Fixme: cache ? but take care to recursion
        if len(self) == 3:
            return Cotation(self[:2])
        else:
            return self

    ##############################################

    @property
    def minor(self):

        if len(self) == 3:
            return self[2]
        else:
            return ''

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
            raise ValueError
        # else:
        #     match.groups() # 0 2

        return str.__new__(cls, chaos_type)

####################################################################################################

class FromJsonMixinMetaClass(type):

    """This metaclass lookup for fields."""

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)

        fields = {}
        for attribute, obj in class_attribute_dict.items():
            if not attribute.startswith('__') and isinstance(obj, (type, InstanceChecker)):
                fields[attribute] = Field(attribute, obj)
        cls.__fields__ = fields
        cls.__field_names__ = sorted([field for field in fields])

####################################################################################################

class FromJsonMixin(metaclass=FromJsonMixinMetaClass):

    """This mixin class implements the import/export to JSON."""

    __fields__ = {}
    __field_names__ = []

    ##############################################

    def __init__(self, **kwargs):

        # Set and check given fields
        for key, value in kwargs.items():
            if key not in self.__field_names__:
                raise ValueError('Unknown key {}'.format(key))
            factory = self.__fields__[key].factory
            # print(key, value, factory)
            if value is not None:
                if isinstance(value, dict):
                    value = factory(**value)
                elif isinstance(value, list):
                    value = factory(*value)
                else:
                    value = factory(value)
            setattr(self, key, value)
        
        # Set to None missing fields
        for key in self.__field_names__:
            if key not in kwargs:
                setattr(self, key, None)

    ##############################################

    def str_long(self):

        return '\n'.join(['{}: {}'.format(field, self.__dict__[field])]
                         for field in self.__field_names__)

    ##############################################

    def to_json(self, only_defined=False):

        d = {}
        for field in self.__field_names__:
            value = self.__dict__[field]
            if hasattr(value, '__json_interface__'):
                value = value.__json_interface__
            if not only_defined or value is not None:
                d[field] = value
        
        return d

####################################################################################################

class Coordinate(FromJsonMixin):

    """This class defines a coordinate."""

    longitude = float
    latitude = float

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

    @property
    def __json_interface__(self):
        return self.to_json()

    @property
    def __geo_interface__(self):
        return {'type': 'Point', 'coordinates': (self.longitude, self.latitude)}

####################################################################################################

class WithCoordinate(FromJsonMixin):

    """Base class for :class:`Massif` and :class:`Circuit`."""

    coordonne = None # Fixme: metaclass don't see this attribute

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(**kwargs)
        self.bleau_database = bleau_database

    ##############################################

    @property
    def __geo_interface__(self):

        properties = self.to_json()
        del properties['coordonne']
        
        return {'type': 'Feature', 'geometry': self.coordonne, 'properties': properties}

    ##############################################

    def __lt__(self, other):

        """ Compare name using French collation """

        # return locale.strcoll(str(self), str(other))
        return locale.strxfrm(str(self)) < locale.strxfrm(str(other))

    ##############################################

    def nearest(self, number_of_items=1, distance_max=None):

        # Fixme: call nearest_massif
        return self.bleau_database.nearest_massif(self, number_of_items, distance_max)

    ##############################################

    def distance_to(self, item):

        x0, y0 = self.coordonne.mercator
        x1, y1 = item.coordonne.mercator
        return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

####################################################################################################

class Place(WithCoordinate):

    """This class defines a place."""

    coordonne = Coordinate
    nom = str
    type = PlaceType # Note: redefine type in this scope!
    notes = str # aka commentaire

####################################################################################################

class Massif(WithCoordinate):

    """This class defines a « massif »."""

    a_pieds = bool
    acces = str
    coordonne = Coordinate
    massif = str
    nom = str
    notes = str
    parcelles = str
    parking = str
    point_deau = str
    rdv = str
    secteur = str
    type_de_chaos = ChaosType
    velo = str
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

        # return iter(sorted(self._circuits, key=lambda x: x.cotation))
        # return iter(sorted(self._circuits, key=lambda x: int(x.cotation)))
        return iter(sorted(self._circuits))

    ##############################################

    def __str__(self):
        return self.massif

    ##############################################

    @property
    def nom_or_massif(self):

        # Fixme: purpose ?
        if self.nom:
            return self.nom
        else:
            return self.massif

    ##############################################

    @property
    def cotations(self):

        return tuple([circuit.cotation for circuit in self])

    ##############################################

    @property
    def uniq_cotations(self):

        # set lost order
        cotations = {circuit.cotation for circuit in self._circuits}
        return tuple(sorted(cotations))

    ##############################################

    @property
    def major_cotations(self):

        cotations = {circuit.cotation.major for circuit in self._circuits}
        return tuple(sorted(cotations))

####################################################################################################

class Circuit(WithCoordinate):

    """This class defines a « circuit »."""

    annee_refection = int
    coordonne = Coordinate
    cotation = Cotation
    couleur = str
    gestion = str
    liste_blocs = StringList
    massif = InstanceChecker(Massif)
    numero = int
    status = str
    topos = StringList
    # patiné

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(bleau_database, **kwargs)
        
        self.massif.add_circuit(self)

    ##############################################

    def __str__(self):
        return '{0.massif}-{0.numero}-{0.cotation}'.format(self)

    ##############################################

    def __lt__(self, other):

        cotation1 = self.cotation
        cotation2 = other.cotation
        if cotation1 == cotation2:
            return self.numero < other.numero
        else:
            return cotation1 < cotation2

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

class BleauDataBase:

    """This class represents the database."""

    ##############################################

    def __init__(self, json_file=None, country_code='fr_FR'):

        # To sort string using French collation
        locale.setlocale(locale.LC_ALL, country_code)
        
        self._rtree_place = None
        self._rtree_massif = None
        self._rtree_circuit = None
        self._ids = {}
        
        if json_file is not None:
            with open(json_file, encoding='utf8') as f:
                data = json.load(f)
            
            places = [Place(self, **place_dict) for place_dict in data['places']]
            self._places = {}
            for place in places:
                self.add_place(place)

            massifs = [Massif(self, **massif_dict) for massif_dict in data['massifs']]
            self._massifs = {}
            for massif in massifs:
                self.add_massif(massif)
            
            self._circuits = []
            for circuit_dict in data['circuits']:
                circuit_dict['massif'] = self._massifs[circuit_dict['massif']]
                self.add_circuit(Circuit(self, **circuit_dict))
        else:
            self._places = {}
            self._massifs = {}
            self._circuits = []

    ##############################################

    # def __del__(self):

    #     del self._rtree

    ##############################################

    @property
    def number_of_circuits(self):
        return len(self._circuits)

    @property
    def number_of_circuits_with_topos(self):
        return len([circuit for circuit in self._circuits
                    if circuit.has_topo()])

    @property
    def number_of_massifs(self):
        return len(self._massifs)

    @property
    def places(self):
        return iter(sorted(self._places.values()))

    @property
    def massifs(self):
        return iter(sorted(self._massifs.values()))

    @property
    def circuits(self):
        return iter(sorted(self._circuits))

    @property
    def secteurs(self):
        # Fixme: unsorted massif iter
        return sorted({massif.secteur for massif in self._massifs.values()})
                      # if massif.secteur is not None

    ##############################################

    def __getitem__(self, key):

        # Fixme: only massif
        return self._massifs[key]

    ##############################################

    def add_place(self, place):

        self._places[str(place)] = place

    ##############################################

    def add_massif(self, massif):

        self._massifs[str(massif)] = massif

    ##############################################

    def add_circuit(self, circuit):

        self._circuits.append(circuit)

    ##############################################

    def to_json(self, json_file=None):

        data = {
            'places': [place.to_json() for place in self.places],
            'massifs': [massif.to_json() for massif in self.massifs],
            'circuits': [circuit.to_json() for circuit in self._circuits], # don't sort circuits
        }

        kwargs = dict(indent=2, ensure_ascii=False, sort_keys=True)
        if json_file is not None:
            with open(json_file, 'w', encoding='utf8') as f:
                json.dump(data, f, **kwargs)
        else:
            return json.dumps(data, **kwargs)

    ##############################################

    def to_geojson(self, json_file=None, places=True, massifs=True, circuits=True):

        features = []
        if places:
            features.extend([place for place in self.places if place.coordonne is not None])
        if massifs:
            features.extend([massif for massif in self.massifs if massif.coordonne is not None])
        if circuits:
            features.extend([circuit for circuit in self.circuits if circuit.coordonne is not None])
        feature_collections = geojson.FeatureCollection(features)
        if not geojson.is_valid(feature_collections):
            raise ValueError
        # Fixme: crs geojson.named API
        
        kwargs = dict(indent=2, ensure_ascii=False, sort_keys=True)
        if json_file is not None:
            with open(json_file, 'w', encoding='utf8') as f:
                geojson.dump(feature_collections, f, **kwargs)
        else:
            return geojson.dumps(feature_collections, **kwargs)

    ##############################################

    def _build_rtree(self, items):

        if rtree is None:
            raise NotImplementedError
        
        rtree_ = rtree.index.Index()
        for item in items:
            if item.coordonne is not None:
                rtree_.insert(id(item), item.coordonne.bounding_box, obj=item)
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

    def nearest_massif(self, item, number_of_items=1, distance_max=None):

        number_of_items += 1
        rtree_ = self.rtree_massif
        # Fixme: segfault ???
        # return [x.object for x in rtree.nearest(item.coordonne.bounding_box, number_of_items, objects=True)]
        items = [self._ids[x] for x in rtree_.nearest(item.coordonne.bounding_box, number_of_items)]
        items = [x for x in items if x is not item]
        if distance_max is not None:
            items = [x for x in items if item.distance_to(x) <= distance_max]
        return items

    ##############################################

    def filter_by(self,
                  a_pieds=None,
                  secteurs=None,
                  type_de_chaos=None,
                  cotations=None,
                  major_cotations=None,
    ):

        # print(a_pieds, secteurs, type_de_chaos, cotations, major_cotations)
        massifs = self.massifs
        if a_pieds is not None:
            massifs = [massif for massif in massifs if massif.a_pieds]
        if secteurs is not None:
            # massif.secteur and
            massifs = [massif for massif in massifs if massif.secteur in secteurs]
        if type_de_chaos is not None:
            type_de_chaos = set(type_de_chaos)
            massifs = [massif for massif in massifs if set(massif.type_de_chaos.split('/')) >= type_de_chaos]
        if cotations is not None or major_cotations is not None:
            if cotations is not None:
                cotations = set(cotations)
                massifs = [massif for massif in massifs if set(massif.uniq_cotations) >= cotations]
            else:
                cotations = set(major_cotations)
                massifs = [massif for massif in massifs if set(massif.major_cotations) >= cotations]
        # print(massifs)

        return massifs

####################################################################################################
#
# End
#
####################################################################################################
