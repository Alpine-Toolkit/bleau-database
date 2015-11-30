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

from .Statistics import CircuitStatisticsCache

####################################################################################################

class Model:

    ##############################################

    def __init__(self, application=None):

        self._application = application
        if application is not None:
            self.init_app(application)

    ##############################################

    def init_app(self, application):

        self._application = application
        self._bleau_database = self._application.config['bleau_database']
        self._circuit_statistics_cache = CircuitStatisticsCache()

    ##############################################

    @property
    def bleau_database(self):
        return self._bleau_database

    ##############################################

    @property
    def circuit_statistics_cache(self):
        return self._circuit_statistics_cache

####################################################################################################

model = Model()

####################################################################################################
#
# End
#
####################################################################################################
