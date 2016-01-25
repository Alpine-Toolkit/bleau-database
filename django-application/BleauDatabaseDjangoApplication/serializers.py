####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) 2016 Fabrice Salvaire
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

from rest_framework import serializers

####################################################################################################

from .models import Person, Place, Massif, Circuit, Refection

####################################################################################################

class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Person

####################################################################################################

class PlaceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Place

####################################################################################################

class MassifSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Massif

####################################################################################################

class CircuitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Circuit

####################################################################################################

class RefectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Refection

####################################################################################################
#
# End
#
####################################################################################################
