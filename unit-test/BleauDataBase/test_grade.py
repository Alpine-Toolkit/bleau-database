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

import unittest

####################################################################################################

from BleauDataBase.BleauDataBase import Grade, AlpineGrade

####################################################################################################

class TestGrade(unittest.TestCase):

    def test(self):

        grades = [grade for grade in Grade.grade_iter()]
        sorted_grades = sorted(grades)
        sorted_grades_str = [str(grade) for grade in sorted_grades]
        grades_str = sorted([str(grade) for grade in grades])
        # check lexicographic order match
        self.assertListEqual(sorted_grades_str, grades_str)

        grades = [grade for grade in Grade.old_grade_iter()]
        sorted_grades = sorted(grades)
        sorted_grades_str = [str(x) for x in sorted_grades]
        self.assertListEqual(list(sorted_grades_str[0::3]), [str(x) + '-' for x in range(1, 10)])
        self.assertListEqual(list(sorted_grades_str[1::3]), [str(x) for x in range(1, 10)])
        self.assertListEqual(list(sorted_grades_str[2::3]), [str(x) + '+' for x in range(1, 10)])

        # for grade in grades:
        #     print(grade, grade.standard_grade)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
