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
import re

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

cotation_re = re.compile(r'^(([1-9])([a-c]?)(\-|\+)?)')
alpine_cotation_re = re.compile(r'.* (en|f|pd|ad|d|td|ed)(\-|\+)?.*')

####################################################################################################

def fix_bloc(bloc):

    if bloc['numero'] == "09.9b":
        bloc['numero'] = "9b"

    convert_to(bloc, 'numero', int)

    if not bloc['cotation']:
        match = cotation_re.match(bloc['descriptif'])
        if match is not None:
            cotation = match.group(0)
            descriptif = bloc['descriptif'][len(cotation):]
            if descriptif.startswith('.'):
                descriptif = descriptif[1:].strip()
            bloc['cotation'] = cotation
            bloc['descriptif'] = descriptif

####################################################################################################

def fix_circuit_blocs(circuit):

    old_blocs = circuit['items']
    new_blocs = []
    for bloc in old_blocs:
        cotation = bloc['cotation']
        descriptif = bloc['descriptif']
        numero = bloc['numero']
        if not (descriptif.startswith('(PNG')
                or descriptif.startswith('(SVG')
                or descriptif.startswith('(JPG')
                or descriptif.startswith('(GIF')
                or cotation.startswith('(SVG')
                or cotation.startswith('(PNG')
                or numero == "?. ?"
                or numero == "26 Blanc Enfant n°1"
        ):
            new_blocs.append(bloc)
    circuit['items'] = new_blocs

    for bloc in new_blocs:
        fix_bloc(bloc)

####################################################################################################

def fix_circuit(secteur, massif, circuit):

    convert_to(circuit, 'lat', float)
    convert_to(circuit, 'lon', float)
    convert_to(circuit, 'renove', int)
    convert_to(circuit, 'nombre_de_voie', int)

    name = circuit['name']
    info = circuit['info']

    circuit['numero'] = None
    if 'n°' in info:
        try:
            numero = int(info[info.find('n°')+2:])
            info = info[:info.find('n°')].strip()
            circuit['numero'] = numero
        except:
            pass

    circuit['couleur'] = None
    couleur_match = False
    for couleur in ('blanc', 'jaune', 'orange', 'bleu', 'rouge', 'noir',
                    'amanite', 'caramel', 'fraise', 'mauve', 'rose', 'saumon', 'vert', 'violet'):
        if couleur in name.lower():
            couleur_match = True
            circuit['couleur'] = couleur

    circuit['cotation'] = None
    match = alpine_cotation_re.match(name.lower())
    if match:
        circuit['cotation'] = ''.join([x for x in match.groups() if x]).upper()

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
    if 'items' in circuit:
        fix_circuit_blocs(circuit)
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
