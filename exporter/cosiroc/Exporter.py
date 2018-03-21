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

def get_attribute(attrs, attribute):

    for key, value in attrs:
        if key == attribute:
            return key, value
    return None, None

####################################################################################################

def clean_str(x):

    x = str(x)
    x = x.strip()
    x = x.replace('\n', '')
    x = x.replace('\t', '')
    x = x.replace(' .', '.')
    return x

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

        d = {attribute:clean_str(getattr(self, attribute)) for attribute in self.__attributes__}
        if self:
            d['items'] = [x.to_json() for x in self]

        return d
