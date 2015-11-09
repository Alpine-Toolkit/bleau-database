####################################################################################################
#
# Copyright (C) Salvaire Fabrice 2015
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

import json
import locale
import math
import urllib.request

from collections import OrderedDict

try:
    import rtree
except:
    rtree = None

####################################################################################################

from .Projection import GeoAngle, GeoCoordinate

####################################################################################################

locale.setlocale(locale.LC_ALL, 'fr_FR')

####################################################################################################

class Field:

    ##############################################

    def __init__(self, name, factory):

        self.name = name
        self.factory = factory

####################################################################################################

def instance_checker(class_):

    def checker(obj):
        if isinstance(obj, class_):
            return obj
        else:
            raise ValueError
    
    return checker

####################################################################################################

class StringList(list):

    ##############################################

    def __init__(self, *args):

        super().__init__([str(x) for x in args])

####################################################################################################

class FromJsonMixin:

    __fields__ = ()

    ##############################################

    def __init__(self, **kwargs):

        field_names = [field.name for field in self.__fields__]
        fields = {field.name:field for field in self.__fields__}
        for key, value in kwargs.items():
            if key not in field_names:
                raise ValueError('Unknown key {}'.format(key))
            factory = fields[key].factory
            # print(key, value, factory)
            if value is not None:
                if isinstance(value, dict):
                    value = factory(**value)
                elif isinstance(value, list):
                    value = factory(*value)
                else:
                    value = factory(value)
            setattr(self, key, value)
        for key in fields:
            if key not in kwargs:
                setattr(self, key, None)

    ##############################################

    def to_json(self):

        return OrderedDict([(field.name, self.__dict__[field.name])
                            for field in self.__fields__])

####################################################################################################

class Coordonne(FromJsonMixin):

    __fields__ = (
        Field('longitude', float),
        Field('latitude', float),
    )

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

####################################################################################################

class WithCoordinate(FromJsonMixin):

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(**kwargs)
        self.bleau_database = bleau_database

    ##############################################

    def to_json(self):

        d = super().to_json()
        if d['coordonne'] is not None:
            d['coordonne'] = d['coordonne'].to_json()
        
        return d

    ##############################################

    def __lt__(self, other):

        # return locale.strcoll(str(self), str(other))
        return locale.strxfrm(str(self)) < locale.strxfrm(str(other))

    ##############################################

    def nearest(self, number_of_items=1, distance_max=None):

        return self.bleau_database.nearest_massif(self, number_of_items, distance_max)

    ##############################################

    def distance_to(self, item):

        x0, y0 = self.coordonne.mercator
        x1, y1 = item.coordonne.mercator
        return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

####################################################################################################

class Massif(WithCoordinate):

    __fields__ = (
        Field('acces', str),
        Field('a_pieds', bool),
        Field('coordonne', Coordonne),
        Field('itineraire', str),
        Field('massif', str),
        Field('nom', str),
        Field('notes', str),
        Field('parcelles', str),
        Field('point_deau', str),
        Field('rdv', str),
        Field('secteur', str),
        Field('type_de_chaos', str),
        Field('velo', str),
        # propreté fréquentation exposition débutant
    )

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(bleau_database, **kwargs)
        
        self._circuits = set()

    ##############################################

    def add_circuit(self, circuit):
        self._circuits.add(circuit)

    ##############################################

    def __len__(self):
        return len(self._circuits)

    ##############################################

    def __iter__(self):
        return iter(sorted(self._circuits, key=lambda x: x.cotation_number))

    ##############################################

    @property
    def nom_or_massif(self):

        if self.nom:
            return self.nom
        else:
            return self.massif

    ##############################################

    def __str__(self):
        return self.massif

    ##############################################

    def str_long(self):

        template = '''
massif: {0.massif}
coordonné: {0.coordonne}
type_de_chaos: {0.type_de_chaos}
parcelles: {0.parcelles}
secteur: {0.secteur}
'''
        return template.format(self)

####################################################################################################

_cotation_bases = ('EN', 'F', 'PD', 'AD', 'D', 'TD', 'ED')
_cotations = []
for cotation in _cotation_bases:
    for suffix in '-', '', '+':
        _cotations.append(cotation + suffix)
_cotation_to_number = {cotation:i for i, cotation in enumerate(_cotations)}

class Circuit(WithCoordinate):

    __fields__ = (
        Field('annee_refection', int),
        Field('coordonne', Coordonne),
        Field('cotation', str),
        Field('couleur', str),
        Field('gestion', str),
        Field('liste_blocs', StringList),
        Field('massif', instance_checker(Massif)),
        Field('numero', int),
        Field('status', str),
        Field('topos', StringList),
        # patiné
    )

    ##############################################

    def __init__(self, bleau_database, **kwargs):

        super().__init__(bleau_database, **kwargs)
        
        self.massif.add_circuit(self)

    ##############################################

    def __str__(self):
        return '{0.massif}-{0.numero}-{0.cotation}'.format(self)

    ##############################################

    def str_long(self):

        template = '''
massif: {0.massif}
couleur: {0.couleur}
numéro: {0.numero}
cotation: {0.cotation}
topos: {0.topos}
coordonné: {0.coordonne}
année_réfection: {0.annee_refection}
gestion: {0.gestion}
status: {0.status}
liste_blocs: {0.liste_blocs}
'''
        return template.format(self)

    ##############################################

    @property
    def cotation_number(self):
        return _cotation_to_number[self.cotation]

    ##############################################

    def has_topo(self):

        return bool(self.topos)

    ##############################################

    def upload_topos(self):

        for url in self.topos:
            if url.endswith('.pdf'):
                print('Get', url)
                with urllib.request.urlopen(url) as response:
                    document = response.read()
                    pdf_name = url[url.rfind('/')+1:]
                    with open(pdf_name, 'wb') as f:
                        f.write(document)

    ##############################################

    def to_json(self, bleau_database):

        d = super().to_json()
        d['massif'] = str(d['massif'])
        
        return d

####################################################################################################

class BleauDataBase:

    ##############################################

    def __init__(self, json_file=None):

        self._rtree_massif = None
        self._rtree_circuit = None
        self._ids = {}
        
        if json_file is not None:
            with open(json_file, encoding='utf8') as f:
                data = json.load(f)
            massifs = [Massif(self, **massif_dict) for massif_dict in data['massifs']]
            self._massifs = {}
            for massif in massifs:
                self.add_massif(massif)
            self._circuits = []
            for circuit_dict in data['circuits']:
                circuit_dict['massif'] = self._massifs[circuit_dict['massif']]
                self.add_circuit(Circuit(self, **circuit_dict))
        else:
            self._massifs = {}
            self._circuits = []

    ##############################################

    # def __del__(self):

    #     del self._rtree

    ##############################################

    @property
    def nombre_de_circuits(self):
        return len(self._circuits)

    @property
    def nombre_de_circuits_avec_topos(self):
        return len([circuit for circuit in self._circuits
                    if circuit.has_topo()])

    @property
    def nombre_de_massifs(self):
        return len(self._massifs)

    @property
    def massifs(self):
        return iter(sorted(self._massifs.values()))

    @property
    def circuits(self):
        return iter(sorted(self._circuits))

    ##############################################

    def __getitem__(self, key):

        return self._massifs[key]

    ##############################################

    def add_massif(self, massif):

        self._massifs[str(massif)] = massif

    ##############################################

    def add_circuit(self, circuit):

        self._circuits.append(circuit)

    ##############################################

    def to_json(self, json_file, sort_keys=False):

        data = OrderedDict(
            massifs=[massif.to_json() for massif in self.massifs],
            circuits=[circuit.to_json(self) for circuit in self.circuits],
        )
        
        with open(json_file, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=sort_keys)

    ##############################################

    def _build_rtree(self, items):

        rtree_ = rtree.index.Index()
        for item in items:
            if item.coordonne is not None:
                rtree_.insert(id(item), item.coordonne.bounding_box, obj=item)
                self._ids[id(item)] = item
        return rtree_

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

    def filter_by(self, secteur=None):

        massifs = self.massifs
        if secteur is not None:
            massifs = [massif for massif in massifs if massif.secteur == secteur]
        
        return massifs

####################################################################################################
#
# End
#
####################################################################################################
