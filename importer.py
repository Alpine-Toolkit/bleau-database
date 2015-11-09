####################################################################################################
#
# Script Python pour importer la base de données du Cosiroc au format JSON
#
# Copyright (C) Salvaire Fabrice 2015
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import argparse

from BleauDataBase import BleauDataBase

####################################################################################################

parser = argparse.ArgumentParser(description='Importer')

parser.add_argument('json_file', metavar='json_file',
                    help='JSON file')

parser.add_argument('--get-pdf',
                    action='store_true')

args = parser.parse_args()

####################################################################################################

bleau_database = BleauDataBase(json_file=args.json_file)

print('Nombre de massifs:', bleau_database.nombre_de_massifs)
print('Nombre de circuits:', bleau_database.nombre_de_circuits)
print('Nombre de circuits avec fiches:', bleau_database.nombre_de_circuits_avec_fiches)

# for circuit in bleau_database.circuits:
#     print(circuit)

if args.get_pdf:
    for circuit in bleau_database.circuits:
        circuit.upload_fiches()

####################################################################################################
#
# End
#
####################################################################################################