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

class Item(list):

    ##############################################

    def __init__(self, url='', name=''):

        super().__init__()
        
        self.url = url
        self.name = name

    ##############################################

    def to_json(self):

        d = {'name': self.name, 'url': self.url}
        if self:
            d['items'] = [x.to_json() for x in self]
        
        return d

####################################################################################################

class MyHTMLParser(HTMLParser):

    ##############################################

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self._in_column = False
        self._in_column_list = False
        
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
        return self._secteurs[-1][-1]

    ##############################################

    def to_json(self):

        return [x.to_json() for x in self]

    ##############################################

    def handle_starttag(self, tag, attrs):

        if not self._in_column:
            if tag == 'div':
                key, value = get_attribute(attrs, 'class')
                if key and value == 'column':
                    self._in_column = True
                    self._secteurs.append(Item())
        elif not self._in_column_list:
            if tag == 'div':
                self._in_column_list = True
            elif tag == 'a':
                key, value = get_attribute(attrs, 'href')
                if key:
                    self._current_secteur.url = value
        else:
            if tag == 'a':
                key, value = get_attribute(attrs, 'href')
                if key:
                    self._current_secteur.append(Item(url=value))

    ##############################################

    def handle_endtag(self, tag):

        if tag == 'div':
            if self._in_column_list:
                self._in_column_list = False
            elif self._in_column:
                self._in_column = False

    ##############################################

    def handle_data(self, data):

        data = data.strip()
        if self._in_column_list:
            try:
                self._current_massif.name += data
            except IndexError:
                pass
        elif self._in_column:
            self._current_secteur.name += data

####################################################################################################

request = requests.get('http://bleaulib.org/spip.php?rubrique4&lang=fr')
source = request.text

parser = MyHTMLParser()
parser.feed(source)

# for secteur in parser:
#     print('\n"{0.name}" "{0.url}"'.format(secteur))
#     for massif in secteur:
#         print('  "{0.name}" "{0.url}"'.format(massif))

print(json.dumps(parser.to_json(), indent=2, ensure_ascii=False, sort_keys=True))

####################################################################################################
#
# End
#
####################################################################################################
