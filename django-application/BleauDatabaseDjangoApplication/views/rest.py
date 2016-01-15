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

from rest_framework import viewsets

####################################################################################################

from ..serializers import (PersonSerializer, OpenerSerializer,
                           PlaceSerializer, MassifSerializer, CircuitSerializer)
from ..models import Person, Opener, Place, Massif, Circuit

####################################################################################################

class PersonViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows persons to be viewed or edited.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

####################################################################################################

class OpenerViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows openers to be viewed or edited.
    """

    queryset = Opener.objects.all()
    serializer_class = OpenerSerializer

####################################################################################################

class PlaceViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows places to be viewed or edited.
    """

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

####################################################################################################

class MassifViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows massifs to be viewed or edited.
    """

    queryset = Massif.objects.all()
    serializer_class = MassifSerializer

####################################################################################################

class CircuitViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows circuits to be viewed or edited.
    """

    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

####################################################################################################
#
# End
#
####################################################################################################
