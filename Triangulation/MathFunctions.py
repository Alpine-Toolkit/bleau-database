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

# Fixme: sign_of ?
def sign(x):
    return cmp(x, 0)

####################################################################################################

def trignometric_clamp(x):

    """ Clamp *x* in the range [-1.,1]. """

    if x > 1.:
        return 1.
    elif x < -1.:
        return -1.
    else:
        return x

####################################################################################################

def is_in_trignometric_range(x):
    return -1. <= x <= 1

####################################################################################################
#
# End
#
####################################################################################################
