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

# from django.contrib import admin
from django.contrib.gis import admin
from reversion.admin import VersionAdmin

####################################################################################################

class YourModelAdmin(VersionAdmin):
    pass

####################################################################################################

from .models import (Place, Massif, Circuit,
                     Person, Opener,
                     Refection, RefectionPerson)

@admin.register(Place)
class PlaceAdmin(YourModelAdmin, admin.OSMGeoAdmin): # admin.ModelAdmin
    pass

@admin.register(Massif)
class MassifAdmin(YourModelAdmin, admin.OSMGeoAdmin):
    pass

@admin.register(Circuit)
class CircuitAdmin(YourModelAdmin, admin.OSMGeoAdmin):
    pass

@admin.register(Person)
class PersonAdmin(YourModelAdmin, admin.ModelAdmin):
    pass

@admin.register(Opener)
class OpenerAdmin(YourModelAdmin, admin.ModelAdmin):
    pass

@admin.register(Refection)
class RefectionAdmin(YourModelAdmin, admin.ModelAdmin):
    pass

@admin.register(RefectionPerson)
class RefectionPersonAdmin(YourModelAdmin, admin.ModelAdmin):
    pass

# admin.site.register(Place, VersionAdmin)

####################################################################################################
#
# End
#
####################################################################################################
