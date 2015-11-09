.. |Cosiroc| replace:: Cosiroc
.. _Cosiroc: http://www.cosiroc.fr

.. |GUMS| replace:: GUMS
.. _GUMS: http://www.gumsparis.asso.fr

==============
English Resume
==============

This reposit contains a JSON database of the bouldering area of Fontainebleau (bleau) made from data
of the |Cosiroc|_ and |Gums|_.

JSON URL: https://raw.githubusercontent.com/Cosiroc/bleau-database/master/bleau.json

It also contains a Python module featuring:

* serialising/deserialising of the JSON file
* object oriented API of the database
* spatial search

=======================
Description en Français
=======================

Ce dépôt contient une base de données au format JSON des sites d'escalade de la région de
Fontainebleau (bleau) constitué à partir de données du |Cosiroc|_ et du |Gums|_.

Le format JSON offre plusieurs avantages:

* il permet d'accéder aux données depuis une page web (dynamic HTML),
* il est facilement lisible depuis un language de programmation,
* il peut être réinjecté dans une base de données SQL ou NoSQL.

Un script Python permet de valider et normaliser le fichier.

L'URL du fichier JSON est https://raw.githubusercontent.com/Cosiroc/bleau-database/master/bleau.json

Format du fichier JSON
----------------------

Les clés sont triées par ordres alphabétiques afin de faciliter la comparaison entre versions.

Utiliser cette commande pour générer un fichier JSON validé et « normalisé »:

.. code:: sh

  bin/importer --rewrite=bleau.json bleau-tmp.json

Exemple avec commentaires:

.. code:: json

    {
      "circuits": [
        {
          "annee_refection": 2011,
          "coordonne": {
            "latitude": 48.377501,
            "longitude": 2.519742
          },
	  "cotation": "TD-",
          "couleur": "rouge",
          "gestion": "ONF77",
          "liste_blocs": [],
          "massif": "91_1",
          "numero": 1,
          "status": "liste SNE",
          "topos": [ "<URL>" ]
        },
      ],
      "massifs": [
        {
          "a_pieds": "<BOOLEAN:false|true> accés possible à pieds depuis une gare",
          "acces": "accés en voiture",
          "coordonne": {
            "latitude": 48.37722,
            "longitude": 2.51919
          },
          "itineraire": "<URL Google Map>",
          "massif": "91_1",
          "nom": "nom alternatif du massif",
          "notes": "texte libre",
          "parcelles": "parcelles ONF",
          "point_deau": "où trouver de l'eau potable à proximité",
          "rdv": "rendez-vous GUMS indiquant un cheminement depuis le parking",
          "type_de_chaos": "Classification Cosiroc du type de chaos e.g. E/D",
          "velo": "accés à vélo depuis une gare proche"
        },
      ]
    }

.. End
