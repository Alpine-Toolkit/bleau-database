####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) Salvaire Fabrice 2016
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

from .Vector import Vector

####################################################################################################

class CircleCircleIntersection:

    ##############################################

    def __init__(self, distance, radius1, radius2):

        #     x^2 + y^2 = R1^2   (1)
        # (x-d)^2 + y^2 = R2^2   (2)
        # (x-d)^2 + R1^2 - x^2 = R2^2   (1) in (2)
        # x = (R1^2 - R2^2 + d^2) / 2d
        # y^2 = R1^2 - x^2

        self._x = (radius1**2 - radius2**2 + distance**2) / (2 * distance)

        d = radius1**2 - self._x**2
        if d >= 0:
            self._y = math.sqrt(d)
        else:
            self._y = None

    ##############################################

    def __bool__(self):
        return self._y is not None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def v_plus(self):
        return Vector(self._x, self._y)

    @property
    def v_minus(self):
        return Vector(self._x, -self._y)

####################################################################################################
#
# End
#
####################################################################################################
