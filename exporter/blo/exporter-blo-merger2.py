#! /usr/bin/env python3

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

import json

####################################################################################################

def convert_url(item, categorie='circuit'):

    url = item['url']
    del item['url']
    blo_url = int(url[len('spip.php?' + categorie):])
    item['blo_url'] = blo_url

    return blo_url

####################################################################################################

with open('html-data/blo/json/blo-blocs.json') as f:
    circuit_blocs = json.load(f)

# "date": "",
# "descriptif": "Créé par F. Decarout",
# "items": [
#   {
#     "cotation": "",
#     "descriptif": "Départ Circuit : dalle peu inclinée.",
#     "name": "",
#     "numero": "Départ circuit enfant 8-12 ans"
#   }
# ],
# "name": "Blanc Enfants E",
# "numero": "Validée SNE. n°3",
# "url": "spip.php?circuit1"

bloc_map = {}
for circuit in circuit_blocs:
    blo_url = convert_url(circuit)
    bloc_map[blo_url] = circuit

####################################################################################################

json_path = 'html-data/blo/json/blo.json'
with open(json_path, 'r', encoding='utf8') as f:
    secteurs = json.load(f)

for secteur in secteurs:
    for massif in secteur['items']:
        for circuit in massif['items']:
            print()
            print(circuit['name'], circuit['blo_url'])
            circuit2 = bloc_map[circuit['blo_url']]
            descriptif1 = circuit['descriptif']
            descriptif2 = circuit2['descriptif']
            if descriptif2:
                circuit['descriptif'] = descriptif2
            # if descriptif1 == descriptif2:
            #     print('==')
            # elif descriptif1.endswith('(...)'):
            #     print('<')
            #     print(1, '|'+descriptif1+'|')
            #     print(2, '|'+descriptif2+'|')
            # else:
            #     print(1, '|'+descriptif1+'|')
            #     print(2, '|'+descriptif2+'|')

####################################################################################################

json_path = 'html-data/blo/json/blo2.json'
with open(json_path, 'w', encoding='utf8') as f:
    json.dump(secteurs, f, indent=2, ensure_ascii=False, sort_keys=True)
