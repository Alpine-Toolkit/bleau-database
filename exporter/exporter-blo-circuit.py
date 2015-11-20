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

def get_attribute(attrs, attribute):

    for key, value in attrs:
        if key == attribute:
            return key, value
    return None, None

####################################################################################################

class Target:

    ##############################################

    def __init__(self):

        self._str = ''

    ##############################################

    def __bool__(self):
        return bool(self._str)

    ##############################################

    def __iadd__(self, text):
        self._str += text
        return self

    ##############################################

    def __str__(self):
        return self._str

####################################################################################################

class ToJsonMixin(list):

    __attributes__ = ()

    ##############################################

    def to_json(self):

        d = {attribute:str(getattr(self, attribute)) for attribute in self.__attributes__}
        if self:
            d['items'] = [x.to_json() for x in self]
        
        return d

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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
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
            self._target += data.strip()

####################################################################################################

request = requests.get('http://bleaulib.org/spip.php?circuit94&lang=fr')
source = request.text

parser = MyHTMLParser()
parser.feed(source)

circuit = parser.circuit

# print(circuit.name)
# print(circuit.date)
# print(circuit.numero)
# print(circuit.descriptif)

for bloc in circuit:
    numero = str(bloc.numero)
    if ',' in numero:
        numero, name = numero.split(',')
        bloc.numero = numero.strip()
        bloc.name = name.strip()
    descriptif = str(bloc.descriptif)
    if ',' in descriptif:
        i = descriptif.find(',')
        bloc.cotation = descriptif[:i].strip()
        bloc.descriptif = descriptif[i+1:].strip()

        print(json.dumps(parser.circuit.to_json(), indent=2, ensure_ascii=False, sort_keys=True))

####################################################################################################
#
# End
#
####################################################################################################
