####################################################################################################
#
# Script Python pour exporter la base de données du Cosiroc vers un fichier JSON
#
# Copyright (C) Salvaire Fabrice 2015
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import json
import os

from collections import OrderedDict
from html.parser import HTMLParser

####################################################################################################

def first(x):
    if x:
        return x[0]
    else:
        return None

####################################################################################################

def fr_key(key):
    # return key.replace('_', ' ')
    return key.replace('é', 'e')

####################################################################################################

class Massif:

    ##############################################

    def __init__(self, *args):

        self.massif_id = int(first(args[0]))
        self.massif = first(args[1])
        lon = first(args[2])
        lat = first(args[3])
        if lon:
            longitude = float(lon)
            latitude = float(lat)
            self.coordonné = OrderedDict(longitude=longitude, latitude=latitude)
        else:
            self.coordonné = None # {}
        
        type_de_chaos = first(args[4])
        if type_de_chaos:
            type_de_chaos = type_de_chaos.replace(' ', '')
        else:
            type_de_chaos = ''
        self.type_de_chaos = type_de_chaos
        
        parcelles = first(args[5])
        if not parcelles:
            parcelles = ''
        self.parcelles = parcelles
        
        # self.circuits = first(args[6])

    ##############################################

    def __str__(self):

        template = '''
massif_id: {0.massif_id}
massif: {0.massif}
coordonné: {0.coordonné}
type_de_chaos: {0.type_de_chaos}
parcelles: {0.parcelles}
'''
        # circuits: {0.circuits}
        
        return template.format(self)

    ##############################################

    def to_json(self):

        keys = ('massif', 'coordonné', 'type_de_chaos', 'parcelles')
        return OrderedDict([(fr_key(key), self.__dict__[key]) for key in keys])

####################################################################################################

class Circuit:

    ##############################################

    def __init__(self, *args):

        # print(args)

        page_id = args[0][0]
        prefix = 'http://www.cosiroc.fr/index.php?option=com_fabrik&view=details&formid=3&rowid='
        if page_id.startswith(prefix):
            self.page_id = int(page_id[len(prefix):])
        else:
            raise ValueError
        
        self.massif = args[0][1]
        self.couleur = first(args[1])
        self.numéro = int(first(args[2]))
        self.cotation = first(args[3])
        self.fiches = [url for url in args[4] if url.startswith('http')]
        
        ign = first(args[5])
        if ign:
            ign = dict([x.split('=') for x in ign[ign.find('?')+1:].split('&')])
            if (ign['couleur'].replace('%20', ' ') != self.couleur
                or ign['numero'] != str(self.numéro)):
                raise ValueError
            ign = {key:float(ign[key]) for key in ('lat', 'lon')}
            self.coordonné = OrderedDict(longitude=ign['lon'], latitude=ign['lat'])
        else:
            self.coordonné = None # {}
        
        année_réfection = args[6]
        if année_réfection:
            année_réfection = int(first(année_réfection))
        else:
            année_réfection = None
        self.année_réfection = année_réfection
        
        self.gestion = first(args[7])
        self.status = first(args[8])
        liste_blocs = first(args[10])
        if liste_blocs == '(0)  blocs':
            self.liste_blocs = None # []
        else:
            self.liste_blocs = liste_blocs

    ##############################################

    def __str__(self):

        template = '''
page_id: {0.page_id}
massif: {0.massif}
couleur: {0.couleur}
numéro: {0.numéro}
cotation: {0.cotation}
fiches: {0.fiches}
coordonné: {0.coordonné}
année_réfection: {0.année_réfection}
gestion: {0.gestion}
status: {0.status}
liste_blocs: {0.liste_blocs}
'''
        
        return template.format(self)

    ##############################################

    def to_json(self):

        keys = ('massif', 'couleur', 'numéro', 'cotation', 'fiches', 'coordonné',
                'année_réfection', 'gestion', 'status', 'liste_blocs')
        return OrderedDict([(fr_key(key), self.__dict__[key]) for key in keys])

####################################################################################################

class MyHTMLParser(HTMLParser):

    ##############################################

    def __init__(self, item_factory, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._in_table = False
        self._in_tbody = False
        self._in_row = False
        self._in_column = False

        self._item_factory = item_factory
        self._items = []
        self._item_data = None
        self._column = None

    ##############################################

    @property
    def items(self):
        return self._items

    ##############################################

    def handle_starttag(self, tag, attrs):

        if tag == 'table':
            for key, value in attrs:
                if key == 'id': # and value == 'list_3_com_content_3':
                    self._in_table = True
        elif tag == 'tbody':
            if self._in_table:
                self._in_tbody = True
        elif tag == 'tr':
            if self._in_tbody:
                self._in_row = True
                self._item_data = []
                # print('-'*100)
        elif tag == 'td':
            if self._in_row:
                self._in_column = True
                self._column = []
        
        if self._in_column:
            # print('<{}>'.format(tag))
            for key, value in attrs:
                if key == 'href':
                    # print('href =', value)
                    self._column.append(value)

    ##############################################

    def handle_endtag(self, tag):

        # if self._in_tbody:
        #     print('</{}>'.format(tag))
        
        if tag == 'table':
            self._in_table = False
        elif tag == 'tbody':
            self._in_tbody = False
        elif tag == 'tr':
            self._in_row = False
            if self._item_data is not None:
                first = self._item_data[0][0]
                if not (first.startswith('Total') or first.startswith('Aucun')):
                    self._items.append(self._item_factory(*self._item_data))
        elif tag == 'td':
            if self._in_column:
                self._item_data.append(self._column)
            self._in_column = False

    ##############################################

    def handle_data(self, data):

        if self._in_column:
            data = data.strip()
            if data:
                self._column.append(data)
            #     print(' '*4 + data)

####################################################################################################

parser = MyHTMLParser(Massif)

html_file = os.path.join('html-data', 'massif.html')
with open(html_file) as f:
    source = f.read()
    parser.feed(source)
massifs = parser.items

# for massif in massifs:
#     print(massif)

####################################################################################################

parser = MyHTMLParser(Circuit)

for i in range(1, 5):
    html_file = os.path.join('html-data', 'circuit{}.html'.format(i))
    with open(html_file) as f:
        source = f.read()
        parser.feed(source)
circuits = parser.items

# for circuit in parser.items:
#     print(circuit)

####################################################################################################

data = OrderedDict(
    massifs=[massif.to_json() for massif in massifs],
    circuits=[circuit.to_json() for circuit in circuits],
)
json_file = 'bleau.json'
with open(json_file, 'w', encoding='utf8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False) # , sort_keys=True

####################################################################################################
#
# End
#
####################################################################################################
