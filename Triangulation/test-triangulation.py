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

from Triangulation.Vector import Vector
from Triangulation import TriangulationGeometry, TriangulationForce

####################################################################################################

geometry = TriangulationGeometry(anchor_distance=50,
                                 anchor_angle=30,
                                 webbing_length=150,
                                 webbing_ratio=.45)

triangulation = TriangulationForce(geometry=geometry,
                                   weight=100,
                                   deviation=0)

anchor1 = geometry.anchor1
anchor2 = geometry.anchor2
node_point = geometry.node_point
weight_force = triangulation.weight_force
force1 = triangulation.force1
force2 = triangulation.force2
orientation1 = force1.orientation()
orientation2 = force2.orientation()
print("Anchor2 : {} {}".format(anchor2.x, anchor2.y))
print("Node : {} {}".format(node_point.x, node_point.y))
print("Weight : {} {}".format(weight_force.x, weight_force.y))
print("Force1 : {} {}".format(force1.x, force1.y))
print("Force2 : {} {}".format(force2.x, force2.y))

force_point = node_point + force1
weight_point = node_point + weight_force

####################################################################################################

import numpy as np

import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

figure, axes = plt.subplots()

points = np.array((anchor1, anchor2,
                   node_point, force_point, weight_point))

x_min = np.min(points[:,0])
x_max = np.max(points[:,0])
y_min = np.min(points[:,1])
y_max = np.max(points[:,1])

x_margin = (x_max - x_min) * .1
y_margin = (y_max - y_min) * .1

x_min = x_min - x_margin
x_max = x_max + x_margin
y_min = y_min - y_margin
y_max = y_max + y_margin

axes.axis('equal')
axes.set_xlim(x_min, x_max)
axes.set_ylim(y_min, y_max)

wedge1 = mpatches.Wedge(node_point, triangulation.weight, -180, orientation2, color='red', alpha=.1)
wedge2 = mpatches.Wedge(node_point, triangulation.weight, orientation1, 0, color='red', alpha=.1)
wedge3 = mpatches.Wedge(node_point, triangulation.weight, orientation2, orientation1, color='green', alpha=.1)
for wedge in wedge1, wedge2, wedge3:
    axes.add_patch(wedge)

for point in anchor1, node_point: # , force_point, weight_point
    axes.axvline(point.x)
    axes.axhline(point.y)

line = mlines.Line2D((force_point.x, force_point.x),
                     (node_point.y, weight_point.y))
axes.add_line(line)
# line = mlines.Line2D((weight_point.x, weight_point.x),
#                      (node_point.y, weight_point.y))
# axes.add_line(line)
# line = mlines.Line2D((node_point.x, force_point.x),
#                      (force_point.y, force_point.y))
# axes.add_line(line)
line = mlines.Line2D((node_point.x, force_point.x),
                     (weight_point.y, weight_point.y))
axes.add_line(line)

# Draw force 1
force_line = mlines.Line2D(np.array((node_point.x, force_point.x)),
                           np.array((node_point.y, force_point.y)),
                           color='orange', linewidth=2)
axes.add_line(force_line)

# Draw force 2
force_line = mlines.Line2D(np.array((force_point.x, weight_point.x)),
                           np.array((force_point.y, weight_point.y)),
                           color='magenta', linewidth=2)
axes.add_line(force_line)

# Draw weight
weight_line = mlines.Line2D(np.array((node_point.x, weight_point.x)),
                            np.array((node_point.y, weight_point.y)),
                            color='red', linewidth=3)
axes.add_line(weight_line)

# Draw webbing
geometry_line = mlines.Line2D((0, anchor2.x),
                              (0, anchor2.y),
                              color='black')
axes.add_line(geometry_line)
geometry_line = mlines.Line2D((0, node_point.x, anchor2.x),
                              (0, node_point.y, anchor2.y),
                              color='black', marker='o', linewidth=3)
axes.add_line(geometry_line)
plt.annotate('P1', xy=anchor1, xytext=anchor1 + Vector.from_polar_coordinate(135, 5), horizontalalignment='right')
plt.annotate('P2', xy=anchor2, xytext=anchor2 + Vector.from_polar_coordinate(45, 5))
plt.annotate('N', xy=node_point, xytext=node_point + Vector.from_polar_coordinate(45, 5))

Tp = (node_point + weight_point + weight_point + Vector(-weight_force.x, 0)) / 3
T1 = (node_point + force_point + force_point + Vector(0, -force1.y)) / 3
T2 = (weight_point + force_point + force_point + Vector(0, force2.y)) / 3
Tf = (node_point + force_point + weight_point) / 3

plt.annotate('Tp', xy=node_point, xytext=Tp, horizontalalignment='center')
plt.annotate('T1', xy=node_point, xytext=T1, horizontalalignment='center')
plt.annotate('T2', xy=node_point, xytext=T2, horizontalalignment='center')
plt.annotate('Tf', xy=node_point, xytext=Tf, horizontalalignment='center')

plt.show()
