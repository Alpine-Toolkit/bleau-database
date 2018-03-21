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

from .BleauDataBase import AlpineGrade, Grade

####################################################################################################

class CounterMixin:

    ##############################################

    def __init__(self, count=0):

        self._count = count

    ##############################################

    @property
    def count(self):
        return self._count

    ##############################################

    def increment(self):
        self._count += 1

####################################################################################################

class GradeCounter(Grade, CounterMixin):

    ##############################################

    def __init__(self, grade, count=0):

        Grade.__init__(self, grade)
        CounterMixin.__init__(self, count)

####################################################################################################

class AlpineGradeCounter(AlpineGrade, CounterMixin):

    ##############################################

    def __init__(self, grade, count=0):

        AlpineGrade.__init__(self, grade)
        CounterMixin.__init__(self, count)

####################################################################################################

class GradeHistogram:

    __grade_class__ = Grade
    __grade_counter_class__ = GradeCounter

    ##############################################

    def __init__(self):

        self._grades = [self.__grade_counter_class__(grade)
                        for grade in self.__grade_class__.grade_iter()]
        self._grade_map = {str(grade):grade for i, grade in enumerate(self._grades)}

    ##############################################

    def __iter__(self):
        return iter(self._grades)

    ##############################################

    def increment(self, grade):
        self._grade_map[str(grade)].increment()

    ##############################################

    def domain(self):

        inf = 10
        sup = 0
        for i, grade_counter in enumerate(self._grades):
            if grade_counter.count:
                inf = min(inf, i)
                sup = max(sup, i)

        return self._grades[inf:sup +1]

####################################################################################################

class AlpineGradeHistogram(GradeHistogram):

    __grade_class__ = AlpineGrade
    __grade_counter_class__ = AlpineGradeCounter

####################################################################################################

class CircuitStatistics:

    ##############################################

    def __init__(self, circuits):

        circuit_grade_histogram = AlpineGradeHistogram()
        global_boulder_grade_histogram = GradeHistogram()
        boulder_grade_histogram_map = {}
        for circuit in circuits:
            circuit_grade_histogram.increment(circuit.grade)
            major_grade = str(circuit.grade.major)
            if major_grade not in boulder_grade_histogram_map:
                boulder_grade_histogram_map[major_grade] = GradeHistogram()
            boulder_grade_histogram = boulder_grade_histogram_map[major_grade]
            boulders = circuit.boulders
            if boulders:
                for boulder in boulders:
                    grade = boulder.grade
                    if grade:
                        standard_grade = str(grade.standard_grade)
                        global_boulder_grade_histogram.increment(standard_grade)
                        boulder_grade_histogram.increment(standard_grade)

        self._circuit_grade_histogram = circuit_grade_histogram
        self._global_boulder_grade_histogram = global_boulder_grade_histogram
        self._boulder_grade_histogram_map = boulder_grade_histogram_map

    ##############################################

    @property
    def circuit_grade_histogram(self):
        return self._circuit_grade_histogram

    ##############################################

    @property
    def global_boulder_grade_histogram(self):
        return self._global_boulder_grade_histogram

    ##############################################

    @property
    def circuit_grades(self):
        return list(self._boulder_grade_histogram_map.keys())

    ##############################################

    def boulder_grade_histogram(self, grade):
        return self._boulder_grade_histogram_map[grade]
