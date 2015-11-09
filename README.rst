.. |Cosiroc| replace:: Cosiroc
.. _Cosiroc: http://www.cosiroc.fr

.. |GUMS| replace:: GUMS
.. _GUMS: http://www.gumsparis.asso.fr

==============
English Resume
==============

This reposit contains a JSON database of the bouldering area of Fontainebleau (bleau) made from data
of the |Cosiroc|_ and |Gums|_.

It also contains a Python module featuring:

* serialising/deserialising of the JSON file
* object oriented API of the database
* spatial search

=======================
Description en Français
=======================

Ce dépôt contient une base de données au format JSON des sites d'escalade de la région de
Fontainebleau (bleau) constitué à partir de données du |Cosiroc|_ et du |Gums|_.

Format du fichier JSON:

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
          "a_pieds": false, # accés possible à pieds depuis une gare
          "acces": "accés en voiture",
          "coordonne": {
            "latitude": 48.37722,
            "longitude": 2.51919
          },
          "itineraire": "<URL Google Map>",
          "massif": "91_1",
          "nom": "nom alternatif",
          "notes": "",
          "parcelles": "parcelles ONF",
          "point_deau": "où trouver de l'eau potable à proximité",
          "rdv": "rendez-vous GUMS",
          "type_de_chaos": "Classification Cosiroc e.g. E/D",
          "velo": "accés à vélo"
        },
      ]
    }

.. End
