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

from rest_framework import viewsets, permissions

####################################################################################################

from ..serializers import (
    CircuitSerializer,
    MassifSerializer,
    PersonSerializer,
    PlaceSerializer,
    RefectionSerializer,
)

from ..models import (
    Circuit,
    Massif,
    Person,
    Place,
    Refection,

####################################################################################################

class CircuitViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

####################################################################################################

class MassifViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Massif.objects.all()
    serializer_class = MassifSerializer

####################################################################################################

class PersonViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

####################################################################################################

class PlaceViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

####################################################################################################

class RefectionViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Refection.objects.all()
    serializer_class = RefectionSerializer

####################################################################################################
#
# End
#
####################################################################################################
