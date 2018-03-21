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

class Circuit(ToJsonMixin):

    __attributes__ = ('name', 'url', 'date', 'numero', 'descriptif')

    ##############################################

    def __init__(self):

        super().__init__()

        self.url = ''
        self.name = Target()
        self.date = Target()
        self.numero = Target()
        self.descriptif = Target()

####################################################################################################

class Bloc(ToJsonMixin):

    __attributes__ = ('name', 'numero', 'descriptif', 'cotation')

    ##############################################

    def __init__(self):

        super().__init__()

        self.name = Target()
        self.numero = Target()
        self.cotation = Target()
        self.descriptif = Target()

####################################################################################################

class MyHTMLParser(HTMLParser):

    ##############################################

    def __init__(self):

        super().__init__(convert_charrefs=True)

        self.circuit = Circuit()

        self._in_bloc = False
        self._target = None

    ##############################################

    @property
    def _current_bloc(self):
        return self.circuit[-1]

    ##############################################

    def handle_starttag(self, tag, attrs):

        if self._in_bloc and tag == 'a':
            self._target = self._current_bloc.numero
        elif tag == 'h2' and not self.circuit.name:
            self._target = self.circuit.name
        elif tag == 'div' and self.circuit.name:
            key, value = get_attribute(attrs, 'class')
            if key and value == 'texte surlignable':
                if self.circuit.numero:
                    self._target = self.circuit.descriptif
                elif self.circuit.date:
                    self._target = self.circuit.numero
        elif tag == 'li' and self.circuit.name:
            self._in_bloc = True
            self.circuit.append(Bloc())

    ##############################################

    def handle_endtag(self, tag):

        if self._in_bloc and tag == 'a':
            self._target = self._current_bloc.descriptif
        elif tag == 'h2' and not self.circuit.date:
            self._target = self.circuit.date
        elif tag == 'li':
            self._in_bloc = False
            self._target = None

    ##############################################

    def handle_data(self, data):

        if self._target is not None:
            self._target += data #.strip()

####################################################################################################

def upload_circuit(url):

    request = requests.get('http://bleaulib.org/' + url)
    source = request.text

    parser = MyHTMLParser()
    parser.feed(source)

    circuit = parser.circuit

    # print(circuit.name)
    # print(circuit.date)
    # print(circuit.numero)
    # print(circuit.descriptif)

    circuit.url = url

    for bloc in circuit:
        numero = str(bloc.numero)
        if ',' in numero:
            i = numero.find(',')
            bloc.numero = numero[:i].strip()
            bloc.name = numero[i+1:].strip()
        descriptif = str(bloc.descriptif)
        if ',' in descriptif:
            i = descriptif.find(',')
            bloc.cotation = descriptif[:i].strip()
            bloc.descriptif = descriptif[i+1:].strip()

    return circuit.to_json()

####################################################################################################

with open('blo-circuits.json') as f:
    circuits_data = json.load(f)

circuits = []
for secteur in circuits_data:
    for massif in secteur['items']:
        for circuit_data in massif['items']:
            print(circuit_data['url'])
            circuit = upload_circuit(circuit_data['url'])
            circuits.append(circuit)

# print(json.dumps(circuits, indent=2, ensure_ascii=False, sort_keys=True))

json_path = 'blo-blocs.json'
with open(json_path, 'w', encoding='utf8') as f:
    json.dump(circuits, f, indent=2, ensure_ascii=False, sort_keys=True)
