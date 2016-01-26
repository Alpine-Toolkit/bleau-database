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
from django.db.models.signals import post_save
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(verbose_name=_('language'), max_length=4,
                                choices=LANGUAGES, default='fr',
                                blank=True, null=True)

    ##############################################

    def __str__(self):
        return "{0.user}".format(self)

####################################################################################################

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

####################################################################################################

class Place(Model):

    """This class defines a place."""

    CATEGORIES_CHOICES = (
        ('parking', _('parking')),
        ('gare', _('gare')),
        ("point d'eau", _("point d'eau")),
    )

    # creation_date = models.DateTimeField(auto_now_add=True)
    category = CharField(verbose_name=_('category'), choices=CATEGORIES_CHOICES, max_length=30)
    coordinate = PointField(verbose_name=_('coordinate'))
    name = CharField(verbose_name=_('name'), max_length=100)
    note = TextField(verbose_name=_('note'), null=True, blank=True) # aka commentaire

    ##############################################

    def __str__(self):

        return self.name

####################################################################################################

class Person(Model):

    first_name = CharField(verbose_name=_('first name'), max_length=100)
    last_name = CharField(verbose_name=_('last name'), max_length=100)

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

        return self.circuit_set.all()

    ##############################################

    @property
    def refections(self):

        return self.refection_set.order_by('date')

####################################################################################################

class Massif(Model):

    """This class defines a massif."""

    acces = TextField(verbose_name=_('acces'), null=True, blank=True) # Fixme: fr
    alternative_name = CharField(verbose_name=_('alternative name'), max_length=100, null=True, blank=True) # Fixme
    chaos_type = CharField(verbose_name=_('chaos type'), max_length=3, null=True, blank=True)
    coordinate = PointField(verbose_name=_('coordinate'), null=True, blank=True)
    name = CharField(verbose_name=_('name'), max_length=100)
    note = TextField(verbose_name=_('note'), null=True, blank=True)
    parcelles = CharField(verbose_name=_('parcelles'), max_length=50, null=True, blank=True) # Fixme: fr
    rdv = TextField(verbose_name=_('Rdv GUMS'), null=True, blank=True) # Fixme: fr
    secteur = CharField(verbose_name=_('secteur'), max_length=100) # Fixme: fr, entity ?
    velo = TextField(verbose_name=_('velo'), null=True, blank=True) # Fixme: fr, gare

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

    boulders = JSONField(verbose_name=_('boulders'), null=True, blank=True)
    colour = CharField(verbose_name=_('colour'), max_length=50, null=True, blank=True)
    coordinate = PointField(verbose_name=_('coordinate'), null=True, blank=True)
    creation_date = IntegerField(verbose_name=_('creation_date'), null=True, blank=True) # Fixme: opening ?
    gestion = CharField(verbose_name=_('gestion'), max_length=50, null=True, blank=True) # Fixme: fr
    grade = CharField(verbose_name=_('grade'), max_length=3, null=True, blank=True)
    massif = ForeignKey(Massif, verbose_name=_('massif'), on_delete=models.CASCADE)
    note = TextField(verbose_name=_('note'), null=True, blank=True)
    number = IntegerField(verbose_name=_('number'))
    openers = ManyToManyField(Person, verbose_name=_('openers'))
    refection_date = IntegerField(verbose_name=_('refection date'), null=True, blank=True)
    refection_note = TextField(verbose_name=_('refection note'), null=True, blank=True)
    status = CharField(verbose_name=_('status'), max_length=50, null=True, blank=True)
    topos = JSONField(verbose_name=_('topos'), null=True, blank=True)

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
        pattern = '{0.massif} ~ ' + str(_('N° ')) + '{0.number} {0.grade} {0.colour}'
        return pattern.format(self)

####################################################################################################

class Refection(Model):

    circuit = models.ForeignKey(Circuit, verbose_name=_('circuit'))
    date = IntegerField(verbose_name=_('date'), null=True, blank=True)
    note = TextField(verbose_name=_('note'), null=True, blank=True)
    persons = ManyToManyField(Person, verbose_name=_('persons'))

    ##############################################

    def __str__(self):
        return '{0.circuit} - {0.date}'.format(self)

####################################################################################################
#
# End
#
####################################################################################################
