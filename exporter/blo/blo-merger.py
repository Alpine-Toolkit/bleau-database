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

def convert_to(item, key, factory):

    try:
        item[key] = factory(item[key])
    except:
        pass

####################################################################################################

def fix_bloc(bloc):

    convert_to(bloc, 'numero', int)
    
    if not bloc['cotation'] and len(bloc['descriptif']) <= 4:
        cotation = bloc['descriptif']
        if cotation.endswith('.'):
            cotation = cotation[:-1]
        bloc['cotation'] = cotation
        bloc['descriptif'] = ''

####################################################################################################

def fix_circuit(secteur, massif, circuit):

    convert_to(circuit, 'lat', float)
    convert_to(circuit, 'lon', float)
    convert_to(circuit, 'renove', int)
    convert_to(circuit, 'nombre_de_voie', int)
    
    circuit['secteur'] = secteur['name']
    circuit['massif'] = massif['name']
    
    blo_url = convert_url(circuit)
    bloc = bloc_map[blo_url] # global
    
    if 'items' in bloc:
        circuit['items'] = bloc['items']
    
    for key in ('name',):
        if circuit[key] != bloc[key]:
            print('!', circuit[key], bloc[key])

####################################################################################################

with open('html-data/blo/json/blo-massifs.json') as f:
    secteurs_and_massifs = json.load(f)

# Make a list of secteurs and massifs
secteur_list1 = []
massif_list1 = []
for secteur in secteurs_and_massifs:
    secteur_list1.append(secteur['name'])
    for massif in secteur['items']:
        massif_list1.append(massif['name'])

####################################################################################################

with open('html-data/blo/json/blo-blocs.json') as f:
    blocs = json.load(f)

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
for circuit in blocs:
    if 'items' in circuit:
        for bloc in circuit['items']:
            fix_bloc(bloc)
    blo_url = convert_url(circuit)
    bloc_map[blo_url] = circuit

####################################################################################################

with open('html-data/blo/json/blo-circuits.json') as f:
    secteurs = json.load(f)

# "cree": "?",
# "descriptif": "Créé par F. Decarout",
# "info": "Validée SNE. n°3",
# "lat": "48.436065",
# "lon": "2.6298",
# "maj": "Octobre 2014",
# "name": "Blanc Enfants E",
# "nombre_de_voie": "1",
# "renove": "0000",
# "status": "",
# "url": "spip.php?circuit1"

secteur_list2 = []
massif_list2 = []
for secteur in secteurs:
    secteur_list2.append(secteur['name'])
    for massif in secteur['items']:
        massif_list2.append(massif['name'])
        convert_url(massif, 'rubrique')
        for circuit in massif['items']:
            fix_circuit(secteur, massif, circuit)

####################################################################################################

# Show difference
print('Secteurs manquants:', set(secteur_list1) - set(secteur_list2))
print('Massifs manquants:', set(massif_list1) - set(massif_list2))

####################################################################################################

json_path = 'html-data/blo/json/blo.json'
with open(json_path, 'w', encoding='utf8') as f:
    json.dump(secteurs, f, indent=2, ensure_ascii=False, sort_keys=True)

####################################################################################################
#
# End
#
####################################################################################################
