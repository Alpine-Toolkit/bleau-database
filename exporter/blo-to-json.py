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

from BleauDataBase.BleauDataBase import Boulder

####################################################################################################

with open('html-data/blo/json/blo.json') as f:
    secteurs = json.load(f)

boulders = []
for secteur in secteurs:
    for massif in secteur['items']:
        if massif['name'] == 'Canche aux Merciers':
            for circuit in massif['items']:
                if circuit['name'] == 'Rouge TD+':
                    for boulder in circuit['items']:
                        d = boulder
                        boulder = Boulder(None,
                                    numero=d['numero'],
                                    name=d['name'],
                                    cotation=d['cotation'],
                                    comment=d['descriptif'])
                        boulders.append(boulder)

boulders.sort()
boulders = [boulder.to_json() for boulder in boulders]
print(json.dumps(boulders, indent=2, ensure_ascii=False, sort_keys=True))

####################################################################################################
#
# End
#
####################################################################################################
