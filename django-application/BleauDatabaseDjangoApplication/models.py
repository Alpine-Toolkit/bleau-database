####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) 2016 Fabrice Salvaire
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

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.db import models
from django.contrib.gis.db.models import (Model,
                                          ForeignKey,
                                          IntegerField,
                                          CharField, TextField,
                                          PointField,
                                          ManyToManyField)

####################################################################################################

from .settings import LANGUAGES
from .utils import strip_accent

####################################################################################################

class Profile(models.Model):

    """This class defines a user profile."""

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    user = models.OneToOneField(User)
    language = models.CharField(max_length=4, blank=True, null=True, choices=LANGUAGES)

    ##############################################

    def __str__(self):
        return "{0.user}".format(self)

####################################################################################################

class Place(Model):

    """This class defines a place."""

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    CATEGORIES_CHOICES = (
        ('parking', _('parking')),
        ('gare', _('gare')),
        ("point d'eau", _("point d'eau")),
    )

    # creation_date = models.DateTimeField(auto_now_add=True)
    category = CharField(choices=CATEGORIES_CHOICES, max_length=30)
    coordinate = PointField()
    name = CharField(max_length=100)
    note = TextField(null=True, blank=True) # aka commentaire

    ##############################################

    def __str__(self):

        return self.name

####################################################################################################

class Person(Model):

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    ##############################################

    def __str__(self):

        return self.name

    ##############################################

    @property
    def name(self):

        return ' '.join((self.first_name, self.last_name))

    ##############################################

    @property
    def last_first_name(self):

        return ' '.join((self.last_name, self.first_name))

    ##############################################

    @property
    def first_letter(self):

        return strip_accent(self.last_name[0].lower())

    ##############################################

    @property
    def opened_circuits(self):

        return self.circuits.all()

    ##############################################

    @property
    def refections(self):

        return self.refection_set.order_by('date')

####################################################################################################

class Massif(Model):

    """This class defines a massif."""

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    acces = TextField(null=True, blank=True) # Fixme: fr
    alternative_name = CharField(max_length=100, null=True, blank=True) # Fixme
    chaos_type = CharField(max_length=3, null=True, blank=True)
    coordinate = PointField(null=True, blank=True)
    name = CharField(max_length=100)
    note = TextField(null=True, blank=True)
    parcelles = CharField(max_length=50, null=True, blank=True) # Fixme: fr
    rdv = TextField(null=True, blank=True) # Fixme: fr
    secteur = CharField(max_length=100) # Fixme: fr, entity ?
    velo = TextField(null=True, blank=True) # Fixme: fr, gare

    ##############################################

    def __str__(self):

        return self.name

    ##############################################

    @property
    def first_letter(self):

        return strip_accent(self.name[0].lower())

    ##############################################

    @property
    def circuits(self):

        return self.circuit_set.order_by('number')

####################################################################################################

class Circuit(Model):

    """This class defines a circuit."""

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    boulders = JSONField(null=True, blank=True)
    colour = CharField(max_length=50, null=True, blank=True)
    coordinate = PointField(null=True, blank=True)
    creation_date = IntegerField(null=True, blank=True) # Fixme: opening ?
    gestion = CharField(max_length=50, null=True, blank=True) # Fixme: fr
    grade = CharField(max_length=3, null=True, blank=True)
    massif = ForeignKey(Massif, on_delete=models.CASCADE)
    note = TextField(null=True, blank=True)
    number = IntegerField()
    openers = ManyToManyField(Person)
    refection_date = IntegerField(null=True, blank=True)
    refection_note = TextField(null=True, blank=True)
    status = CharField(max_length=50, null=True, blank=True)
    topos = JSONField(null=True, blank=True)

    ##############################################

    def __str__(self):
        return '{0.massif}-{0.number}'.format(self)

    ##############################################

    @property
    def name(self):
        return 'N° {0.number}'.format(self)

    ##############################################

    @property
    def full_name(self):
        pattern = '{0.massif} ' + _('N° ') + '{0.number} {0.grade} {0.colour}'
        return pattern.format(self)

####################################################################################################

class Refection(Model):

    class Meta:
        app_label = 'BleauDatabaseDjangoApplication'

    circuit = models.ForeignKey(Circuit)
    date = IntegerField(null=True, blank=True)
    note = TextField(null=True, blank=True)
    persons = ManyToManyField(Person)

    ##############################################

    def __str__(self):
        return '{0.circuit} - {0.date}'.format(self)

####################################################################################################
#
# End
#
####################################################################################################
