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

# parser.add_argument('--rewrite',
#                     default=None,
#                     help='Rewrite the JSON database file')

# parser.add_argument('--dont-raise-for-unknown', dest='raise_for_unknown',
#                     action='store_false',
#                     help='')

args = parser.parse_args()

####################################################################################################

# , raise_for_unknown=args.raise_for_unknown
bleau_database = BleauDataBase(json_file=args.json_file)

####################################################################################################

with open('html-data/blo/json/blo.json', encoding='utf8') as f:
    secteurs = json.load(f)

for secteur in secteurs:
    for massif in secteur['items']:
        if massif['name'] not in bleau_database:
            print(massif['name'])

# if args.rewrite is not None:
#     bleau_database.to_json(args.rewrite)
