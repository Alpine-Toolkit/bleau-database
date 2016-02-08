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

from .Vector import Vector
from .Circle import CircleCircleIntersection

####################################################################################################

class TriangulationGeometry:

    ##############################################

    def __init__(self, anchor_distance, anchor_angle, webbing_length, webbing_ratio):

        if webbing_length <= anchor_distance:
            raise NameError("Webbing must be longer than the anchor distance")

        self._anchor_distance = anchor_distance
        self._anchor_angle = anchor_angle
        self._webbing_length = webbing_length
        self._webbing_ratio = webbing_ratio

        self._webbing_length1 = webbing_length * webbing_ratio
        self._webbing_length2 = webbing_length * (1 - webbing_ratio)

        self._anchor2 = Vector.from_polar_coordinate(anchor_angle, anchor_distance)

        intersection = CircleCircleIntersection(anchor_distance, self._webbing_length1, self._webbing_length2)
        if not intersection:
            raise RuntimeError()
        self._node_point = intersection.v_minus.rotate_counter_clockwise(anchor_angle)

    ##############################################

    @property
    def anchor_distance(self):
        return self._anchor_distance

    @property
    def anchor_angle(self):
        return self._anchor_angle

    @property
    def webbing_length(self):
        return self._webbing_length

    @property
    def webbing_ratio(self):
        return self._webbing_ratio

    @property
    def webbing_length1(self):
        return self._webbing_length1

    @property
    def webbing_length2(self):
        return self._webbing_length2

    @property
    def anchor1(self):
        return Vector(0, 0)

    @property
    def anchor2(self):
        return self._anchor2

    @property
    def node_point(self):
        return self._node_point


from .Line import Line
from .Vector import Vector

####################################################################################################

class TriangulationGeometry:

    ##############################################

    def __init__(self, anchor_distance, anchor_angle, webbing_length, webbing_ratio):

        if webbing_length <= anchor_distance:
            raise NameError("Webbing must be longer than the anchor distance")

        self._anchor_distance = anchor_distance
        self._anchor_angle = anchor_angle
        self._webbing_length = webbing_length
        self._webbing_ratio = webbing_ratio

        self._webbing_length1 = webbing_length * webbing_ratio
        self._webbing_length2 = webbing_length * (1 - webbing_ratio)

        self._anchor2 = Vector.from_polar_coordinate(anchor_angle, anchor_distance)

        intersection = CircleCircleIntersection(anchor_distance, self._webbing_length1, self._webbing_length2)
        if not intersection:
            raise RuntimeError()
        self._node_point = intersection.v_minus.rotate_counter_clockwise(anchor_angle)

    ##############################################

    @property
    def anchor_distance(self):
        return self._anchor_distance

    @property
    def anchor_angle(self):
        return self._anchor_angle

    @property
    def webbing_length(self):
        return self._webbing_length

    @property
    def webbing_ratio(self):
        return self._webbing_ratio

    @property
    def webbing_length1(self):
        return self._webbing_length1

    @property
    def webbing_length2(self):
        return self._webbing_length2

    @property
    def anchor1(self):
        return Vector(0, 0)

    @property
    def anchor2(self):
        return self._anchor2

    @property
    def node_point(self):
        return self._node_point

    @property
    def edge1_direction(self):
        return self._node_point.normalised()

    @property
    def edge1_direction(self):
        return self._node_point.to_normalised()

    @property
    def edge2_direction(self):
        return (self._node_point - self._anchor2).to_normalised()

####################################################################################################

class TriangulationForce:

    ##############################################

    def __init__(self, geometry, weight, deviation):

        self._geometry = geometry
        self._weight_magnitude = weight
        self._deviation = deviation
        self._weight_vector = Vector.from_polar_coordinate(-90 + deviation, weight)

        origin = Vector(0, 0)
        line1 = Line(origin, geometry.edge1_direction)
        line2 = Line(self._weight_vector, geometry.edge2_direction)
        s1, s2 = line1.intersection_abscissae(line2)
        self._force1 = line1.point_at_s(s1)
        self._force2 = self._weight_vector - self._force1

    ##############################################

    @property
    def geometry(self):
        return self._geometry

    @property
    def weight(self):
        return self._weight_magnitude

    @property
    def deviation(self):
        return self._deviation

    @property
    def weight_force(self):
        return self._weight_vector

    @property
    def force1(self):
        return self._force1

    @property
    def force2(self):
        return self._force2

####################################################################################################
#
# End
#
####################################################################################################
