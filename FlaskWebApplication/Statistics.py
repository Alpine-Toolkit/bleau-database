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

import hashlib

# from bokeh.plotting import figure
from bokeh.embed import components
from bokeh._legacy_charts import Bar

####################################################################################################

from BleauDataBase.Statistics import CircuitStatistics

####################################################################################################

class BokehPlot:

    ##############################################

    def __init__(self, *args, **kwargs):

        script, div = components(*args, **kwargs)
        self.script = script
        self.div = div

####################################################################################################

class CircuitStatisticsData:

    ##############################################

    def __init__(self, circuits):

        self._circuit_statistics = CircuitStatistics(circuits)
        self._circuit_grade_barchart = self._make_barchart(self._circuit_statistics.circuit_grade_histogram,
                                                           'Cotation des Circuits') # Circuit Grade
        self._global_boulder_grade_barchart = self._make_barchart(self._circuit_statistics.global_boulder_grade_histogram,
                                                                  'Cotations des Blocs') # Boulder Grade
        self._boulder_grade_barchart_map = {grade:self._make_barchart(self._circuit_statistics.boulder_grade_histogram(grade),
                                                                      'Cotations des Blocs pour les circuits {}'.format(grade))
                                            for grade in self._circuit_statistics.circuit_grades}

    ##############################################

    def _make_barchart(self, histogram, title):

        grade_counters = histogram.domain()
        y_data = [grade_counter.count for grade_counter in grade_counters]
        x_data = [str(grade_counter) for grade_counter in grade_counters]
        bar = Bar(y_data, x_data, title=title, stacked=True, tools='')
        bar.toolbar_location = None
        
        return BokehPlot(bar)

    ##############################################

    @property
    def circuit_statistics(self):
        return self._circuit_statistics

    @property
    def circuit_grade_barchart(self):
        return self._circuit_grade_barchart

    @property
    def global_boulder_grade_barchart(self):
        return self._global_boulder_grade_barchart

    @property
    def circuit_grades(self):
        return list(self._boulder_grade_barchart_map.keys())

    def boulder_grade_barchart(self, grade):
        return self._boulder_grade_barchart_map[grade]

####################################################################################################

class CircuitStatisticsCache:

    ##############################################

    def __init__(self):

        self._cache = {}

    ##############################################

    def __getitem__(self, circuits):

        ids = [id(circuit) for circuit in circuits]
        id_string = ''.join([str(x) for x in sorted(ids)])
        key = hashlib.sha256(id_string.encode('ascii'))
        if key not in self._cache:
            self._cache[key] = CircuitStatisticsData(circuits)
        return self._cache[key]

####################################################################################################
#
# End
#
####################################################################################################
