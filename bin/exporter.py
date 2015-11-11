#! /usr/bin/env python3

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

import os

from html.parser import HTMLParser

####################################################################################################

from BleauDataBase.BleauDataBase import Massif, Circuit, BleauDataBase

####################################################################################################

def first(x):
    if x:
        return x[0]
    else:
        return None

####################################################################################################

class MassifExporter:

    ##############################################

    def export(self, *args):

        massif_id = int(first(args[0]))
        massif = first(args[1])
        
        lon = first(args[2])
        lat = first(args[3])
        if lon:
            longitude = float(lon)
            latitude = float(lat)
            coordonne = dict(longitude=longitude, latitude=latitude)
        else:
            coordonne = None
        
        type_de_chaos = first(args[4])
        if type_de_chaos:
            type_de_chaos = type_de_chaos.replace(' ', '')
        else:
            type_de_chaos = ''
        
        parcelles = first(args[5])
        if not parcelles:
            parcelles = ''
        
        circuits = first(args[6])
        
        return Massif(massif=massif,
                      coordonne=coordonne,
                      type_de_chaos=type_de_chaos,
                      parcelles=parcelles)

####################################################################################################

class CircuitExporter:

    ##############################################

    def __init__(self, bleau_database):

        self._bleau_database = bleau_database

    ##############################################

    def export(self, *args):

        page_id = args[0][0]
        prefix = 'http://www.cosiroc.fr/index.php?option=com_fabrik&view=details&formid=3&rowid='
        if page_id.startswith(prefix):
            page_id = int(page_id[len(prefix):])
        else:
            raise ValueError
        
        massif = args[0][1]
        couleur = first(args[1])
        numero = int(first(args[2]))
        cotation = first(args[3])
        topos = [url for url in args[4] if url.startswith('http')]
        
        ign = first(args[5])
        if ign:
            ign = dict([x.split('=') for x in ign[ign.find('?')+1:].split('&')])
            if (ign['couleur'].replace('%20', ' ') != couleur
                or ign['numero'] != str(numero)):
                raise ValueError
            ign = {key:float(ign[key]) for key in ('lat', 'lon')}
            coordonne = dict(longitude=ign['lon'], latitude=ign['lat'])
        else:
            coordonne = None
        
        annee_refection = args[6]
        if annee_refection:
            annee_refection = int(first(annee_refection))
        else:
            annee_refection = None
        
        gestion = first(args[7])
        status = first(args[8])
        liste_blocs = first(args[10])
        if liste_blocs == '(0)  blocs':
            liste_blocs = None # []
        else:
            liste_blocs = liste_blocs
        
        return Circuit(massif=self._bleau_database[massif],
                       couleur=couleur,
                       numero=numero,
                       cotation=cotation,
                       topos=topos,
                       coordonne=coordonne,
                       annee_refection=annee_refection,
                       gestion=gestion,
                       status=status,
                       liste_blocs=liste_blocs,
        )

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
                    self._items.append(self._item_factory.export(*self._item_data))
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

bleau_database = BleauDataBase()

parser = MyHTMLParser(MassifExporter())
html_file = os.path.join('html-data', 'massif.html')
with open(html_file) as f:
    source = f.read()
    parser.feed(source)
for massif in parser.items:
    bleau_database.add_massif(massif)

parser = MyHTMLParser(CircuitExporter(bleau_database))
for i in range(1, 5):
    html_file = os.path.join('html-data', 'circuit{}.html'.format(i))
    with open(html_file) as f:
        source = f.read()
        parser.feed(source)
for circuit in parser.items:
    bleau_database.add_circuit(circuit)

json_file = 'bleau-raw.json'
bleau_database.to_json(json_file)

####################################################################################################
#
# End
#
####################################################################################################
