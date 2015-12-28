####################################################################################################

import argparse
import json

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

alternative_name = {
    # "Apremont Varrapeurs": "", # ?
    # "Franchard Meyer": "", # ?
    # "Franchard Raymond": "", # ?
    # "Cuvier Ouest": "", # ?
    # "Le Calvaire": "", # ?
    # "Le Requin": "", # ?
    # "Mont Sarrasin": "", # ?
    # "Rocher du Duc - Sud-Est": "", # sud nainville ?
    "Bas Cuvier": "Cuvier Bas",
    "Buthiers - Massif de L’I": "Buthiers L'I",
    "Butte aux Dames": "Apremont Dames",
    "Chamarande Belvédère": "Chamarande",
    "Corne-Biche, R. de Milly": "Rocher de Milly - Corne-Biche",
    "Désert d’Apremont": "Apremont Désert",
    "Envers d’Apremont": "Apremont Envers",
    "Gorges du Houx Petit Paradis": "Gorges du Houx",
    "Gros Sablons Nord": "Gros Sablons",
    "Hautes Plaines": "Franchard Hautes-Plaines",
    "J.A. Martin": "J.A. Martin - R. Cailleau",
    "La Feuillardière": "Feuillardière",
    "La Padôle": "Padôle",
    "La Ségognole": "Ségognole",
    "L’ Éléphant": "Éléphant",
    "Le Pendu d’Huison": "Pendu d'Huison",
    "Le Sanglier": "Sanglier",
    "Les Gorges d’Apremont": "Apremont Gorges",
    "Le Troglodyte": "Troglodytes",
    "L’Isatis": "Franchard Isatis",
    "Maisse Tramerolle": "Maisse le Patouillat",
    "Mondeville": "Roche aux Dames - Mondeville",
    "Mont Aigu": "Mont-Aigu",
    "Mont d’Olivet": "Mont Olivet",
    "Mont Ussy": "Mont-Ussy",
    "Petit Bois de Saint-Pierre-lès-Nemours": "Petit Bois de St Pierre de Nemours",
    "Pignon 91.1": "91_1",
    "Pignon  95.2": "95_2",
    "R. Canon": "Rocher Canon",
    "R. de la Cathédrale": "Rocher de la Cathédrale",
    "R. des Demoiselles": "Demoiselles",
    "Restant du Long Rocher Nord": "Restant du Long Rocher",
    "Roche d’Hercule": "Roche Hercule",
    "Rocher d’Avon": "Rocher d'Avon",
    "Rocher d’Avon Ouest": "Rocher d'Avon",
    "Rocher de Châtillon": "Rocher de Chatillon",
    "Rocher des Potêts": "Rocher des Potets",
    "Rocher du Duc - côté Beauvais": "Rocher du Duc - Hameau",
    "Rocher du Duc - côté Loutteville": "Rocher du Duc - Loutteville",
    "Rocher du Duc - côté Nainville": "Rocher du Duc - Nainville",
    "Rocher du Télégraphe": "Télégraphe",
    "Rocher Fin": "Rocher fin",
    "Sablons": "Franchard Sablons",
    "Vallée de la Mée -  Potala": "Potala",
    "Vallon Cassepot": "Vallée Casse-Pot",
    "Videlles-les-Roches": "Videlles les Roches",
    "Villeneuve sur Auvers": "Villeneuve-sur-Auvers",
}

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
                number = number.replace('ex ', '') + ' ex'
            if number.endswith('b'):
                number = number.replace('b', 'bis')
            if number.endswith('t'):
                number = number.replace('t', 'ter')

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
        massif = circuit_blo['massif']
        if massif in alternative_name:
            massif = alternative_name[massif]
        if (massif == circuit.massif.name
            and circuit_blo['numero'] == circuit.number
        ):
            couleur_match = circuit_blo['couleur'] == circuit.colour
            # cotation_match = circuit_blo['cotation'] == circuit.grade
            if couleur_match:
                found_circuit = circuit
            else:
                # !! D D bleu bleu ciel
                # !! PD+ AD+ jaune orange
                # !! AD- AD- jaune orange
                pass
                # print('!!', circuit_blo['cotation'], circuit.grade, circuit_blo['couleur'], circuit.colour)

    # Add boulders
    # if found_circuit is not None and not found_circuit.boulders:
    #     boulders = convert_boulder(circuit_blo)
    #     # print(str(found_circuit), len(boulders))
    #     found_circuit.boulders = boulders
    # else:
    #     pass
        # print('!', circuit_blo['massif'], '|', circuit_blo['name'])
        # print('!',
        #       circuit_blo['massif'],
        #       circuit_blo['numero'], circuit_blo ['cotation'], circuit_blo['couleur'],
        #       number_of_boulders)

    # keys = 'numero', 'renove', 'items', 'cotation', 'descriptif', 'lon', 'cree', 'secteur', 'maj',
    #        'status', 'couleur', 'blo_url', 'name', 'nombre_de_voie', 'info', 'lat', 'massif'

    # keys = set()
    # if found_circuit is not None:
    #     keys |= set(circuit_blo.keys())
    # print(keys)

    if found_circuit:
        print()
        print(found_circuit.name)
        try:
            renove = int(circuit_blo['renove'])
        except:
            renove = 0
        try:
            cree = int(circuit_blo['cree'])
        except:
            cree = 0
        print(cree, renove)
        print(circuit_blo['descriptif'])
        print(circuit_blo['info'])

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

# if args.rewrite is not None:
#     bleau_database.to_json(args.rewrite)

####################################################################################################
#
# End
#
####################################################################################################
