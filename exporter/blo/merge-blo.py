####################################################################################################

import argparse
import json
import re

from BleauDataBase.BleauDataBase import BleauDataBase, Boulder

####################################################################################################

parser = argparse.ArgumentParser(description='Importer')

parser.add_argument('json_file', metavar='json_file',
                    help='JSON database file')

parser.add_argument('blo_json_file', metavar='blo_json_file',
                    help='Blo JSON database file')

parser.add_argument('--rewrite',
                    default=None,
                    help='Rewrite the JSON database file')

parser.add_argument('--dont-raise-for-unknown', dest='raise_for_unknown',
                    action='store_false',
                    help='')

args = parser.parse_args()

####################################################################################################

bleau_database = BleauDataBase(json_file=args.json_file, raise_for_unknown=args.raise_for_unknown)

####################################################################################################

def convert_boulder(circuit_blo):

    boulders = []
    for boulder in circuit_blo['items']:
        d = boulder

        number = d['numero']
        name = d['name']
        grade = d['cotation']
        comment = d['descriptif']

        if not grade:
            grade = None

        if isinstance(number, str):
            if number.startswith('ex '):
                number = number.replace('ex ', '')
                number += 'ex'
            if number.endswith('b'):
                number.replace('b', 'bis')
            if number.endswith('t'):
                number.replace('t', 'ter')

        comment = comment.replace('  ', ' ')
        
        boulder = Boulder(bleau_database,
                          number=number,
                          name=name,
                          grade=grade,
                          comment=comment)
        boulders.append(boulder)
    boulders.sort()
    
    return boulders

####################################################################################################

def merge_circuit(circuit_blo):

    found_circuit = None
    for circuit in bleau_database.circuits:
        # print(circuit.massif, circuit.grade, circuit.colour)
        if (circuit_blo['massif'] == circuit.massif.name
            and circuit_blo['numero'] == circuit.number
        ):
            couleur_match = circuit_blo['couleur'] == circuit.colour
            cotation_match = circuit_blo['cotation'] == circuit.grade
            if couleur_match:
                found_circuit = circuit
            else:
                # !! D D bleu bleu ciel
                # !! PD+ AD+ jaune orange
                # !! AD- AD- jaune orange
                pass
                # print('!!', circuit_blo['cotation'], circuit.grade, circuit_blo['couleur'], circuit.colour)

    if found_circuit is not None:
        boulders = convert_boulder(circuit_blo)
        print(str(found_circuit), len(boulders))
        found_circuit.boulders = boulders
    else:
        pass 
        # print('!',
        #       circuit_blo['massif'],
        #       circuit_blo['numero'], circuit_blo ['cotation'], circuit_blo['couleur'],
        #       number_of_boulders)

####################################################################################################

with open('html-data/blo/json/blo.json', encoding='utf8') as f:
    secteurs = json.load(f)

for secteur in secteurs:
    for massif in secteur['items']:
        for circuit_blo in massif['items']:
            if 'items' in circuit_blo:
                boulders = circuit_blo['items']
                number_of_boulders = len(boulders)
                if number_of_boulders > 1:
                    merge_circuit(circuit_blo)

if args.rewrite is not None:
    bleau_database.to_json(args.rewrite)

####################################################################################################
#
# End
#
####################################################################################################
