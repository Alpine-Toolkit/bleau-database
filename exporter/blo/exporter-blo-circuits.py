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

import json
import requests

from html.parser import HTMLParser

####################################################################################################

from Exporter import get_attribute, Target, ToJsonMixin

####################################################################################################

class Secteur(ToJsonMixin):

    __attributes__ = ('name',)

    ##############################################

    def __init__(self):

        super().__init__()

        self.name = Target()

####################################################################################################

class Massif(ToJsonMixin):

    __attributes__ = ('name', 'url', 'descriptif', 'note')

    ##############################################

    def __init__(self):

        super().__init__()

        self.url = ''
        self.name = Target()
        self.descriptif = Target()
        self.note = Target()

####################################################################################################

class Circuit(ToJsonMixin):

    __attributes__ = ('name', 'url', 'cree', 'renove', 'nombre_de_voie',
                      'status', 'info', 'lon', 'lat', 'descriptif', 'maj')

    ##############################################

    def __init__(self):

        super().__init__()

        self.url = ''
        self.name = Target()
        self.logo = Target()
        self.cree = Target()
        self.renove = Target()
        self.nombre_de_voie = Target()
        self.status = Target()
        self.info = Target()
        self.lon = Target()
        self.lat = Target()
        self.descriptif = Target()
        self.maj = Target()

        self._columns = [
            self.name,
            self.logo,
            self.cree,
            self.renove,
            self.nombre_de_voie,
            self.status,
            self.info,
            self.lon,
            self.lat,
            self.descriptif,
            self.maj,
        ]
        self._column = -1

    ##############################################

    def next_target(self):

        self._column += 1
        return self._columns[self._column]

####################################################################################################

class MyHTMLParser(HTMLParser):

    ##############################################

    def __init__(self):

        super().__init__(convert_charrefs=True)

        self._in_table = False
        self._in_secteur = False
        self._in_secteur_name = False
        self._in_massif = False
        self._in_massif_name = False
        self._in_circuit = False
        self._target = None

        self._secteurs = []

    ##############################################

    def __iter__(self):
        return iter(self._secteurs)

    ##############################################

    @property
    def _current_secteur(self):
        return self._secteurs[-1]

    ##############################################

    @property
    def _current_massif(self):
        return self._current_secteur[-1]

    ##############################################

    @property
    def _current_circuit(self):
        return self._current_massif[-1]

    ##############################################

    def to_json(self):

        return [x.to_json() for x in self]

    ##############################################

    def handle_starttag(self, tag, attrs):

        if not self._in_table:
            if tag == 'tbody':
                self._in_table = True
        else:
            if tag == 'tr':
                key, value = get_attribute(attrs, 'class')
                if key:
                    if value == 'negative':
                        self._in_secteur = True
                        self._secteurs.append(Secteur())
                    elif value == 'positive':
                        self._in_massif = True
                        self._current_secteur.append(Massif())
                else:
                    self._in_circuit = True
                    self._current_massif.append(Circuit())
            else:
                if self._in_circuit:
                    if tag == 'td':
                        self._target = self._current_circuit.next_target()
                    elif tag == 'a':
                        key, value = get_attribute(attrs, 'href')
                        if key:
                            self._current_circuit.url = value
                elif self._in_secteur and tag == 'h1':
                    self._in_secteur_name = True
                    self._target = self._current_secteur.name
                elif self._in_massif:
                    if tag == 'a':
                        self._in_massif_name = True
                        self._target = self._current_massif.name
                        key, value = get_attribute(attrs, 'href')
                        if key:
                            self._current_massif.url = value
                    elif tag == 'div':
                        key, value = get_attribute(attrs, 'class')
                        if key:
                            if value == 'descriptif':
                                self._target = self._current_massif.descriptif
                            else:
                                self._target = self._current_massif.note

    ##############################################

    def handle_endtag(self, tag):

        if self._in_table:
            if tag == 'table':
                self._in_table = False
            elif tag == 'tr':
                if self._in_circuit:
                    self._in_circuit = False
                elif self._in_massif:
                    self._in_massif = False
                if self._in_secteur:
                    self._in_secteur = False
                self._target = None
            elif tag == 'h3':
                self._in_massif_name = False
                self._target = None
            elif tag == 'h1':
                self._in_secteur_name = False
                self._target = None
            elif tag == 'div':
                if self._in_massif and not self._in_circuit:
                    self._target = None

    ##############################################

    def handle_data(self, data):

        if self._target is not None:
            self._target += data.strip()

####################################################################################################

request = requests.get('http://bleaulib.org/spip.php?page=circuits&lang=fr')
source = request.text

parser = MyHTMLParser()
parser.feed(source)

# for secteur in parser:
#     print('\n"{0.name}"'.format(secteur))
#     for massif in secteur:
#         print('  "{0.name}" "{0.url}" "{0.descriptif}" "{0.note}"'.format(massif))

print(json.dumps(parser.to_json(), indent=2, ensure_ascii=False, sort_keys=True))

####################################################################################################
#
# End
#
####################################################################################################
