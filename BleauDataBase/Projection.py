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

import math

####################################################################################################

class GeoAngle(object):

    ##############################################

    @staticmethod
    def to_decimal(degrees, minutes=0, seconds=0):
        return degrees + (minutes + seconds / 60) / 60

    ##############################################

    @staticmethod
    def to_sexagesimal(x):
        f, degrees = math.modf(x)
        f, minutes = math.modf(f * 60)
        # f, second = math.modf(f * 60)
        second = f * 60
        return (int(degrees), int(minutes), second)

    ##############################################

    def __init__(self, degrees, minutes=0, seconds=0):

        self._value = self.to_decimal(degrees, minutes, seconds)

    ##############################################

    def __float__(self):

        return self._value

    ##############################################

    def __str__(self):

        return str(self._value)

    ##############################################

    @property
    def decimal(self):

        return self._value

    ##############################################

    @property
    def sexagesimal(self):

        return self.to_sexagesimal(self._value)

####################################################################################################

# WGS 84, WGS 1984, EPSG:4326

class GeoCoordinate(object):

    # Equatorial radius (half major axis) of the ellipsoid
    equatorial_radius = 6378137.0 # m

    ##############################################

    def __init__(self, longitude, latitude):

        self.latitude = latitude
        self.longitude = longitude

    ##############################################

    @property
    def mercator(self):

        # epsg:3857
        
        x = math.radians(float(self.longitude.decimal))
        y = math.log(math.tan(math.radians(self.latitude.decimal)/2 + math.pi/4))
        x *= self.equatorial_radius
        y *= self.equatorial_radius
        # y = R/2 * math.log((1 + math.sin(latitude))/(1 - math.sin(latitude))
        
        return (x, y)

    ##############################################

    def __str__(self):

        return "{}, {}".format(self.longitude, self.latitude)

####################################################################################################
#
# End
#
####################################################################################################
