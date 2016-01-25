####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) Salvaire Fabrice 2016
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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.utils.translation import ugettext as _

####################################################################################################

from ..models import Circuit, Person

####################################################################################################

class CircuitForm(ModelForm):

    class Meta:
        model = Circuit
        fields = (
            'number',
            'colour',
            'grade',
            'coordinate',
            'gestion',
            'status',
            'creation_date',
            'refection_date',
            'refection_note',
            'note',
            'topos',
            # 'massif',
        )

    coordinate = CharField(max_length=100)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(CircuitForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = CircuitForm(request.POST)
        if form.is_valid():
            circuit = form.save(commit=False)
            circuit.save()
            messages.success(request, "Circuit créé avec succès.")
            return HttpResponseRedirect(reverse('circuits.details', args=[circuit.pk]))
        else:
            messages.error(request, "Des informations sont manquantes ou incorrectes")
    else:
        form = CircuitForm()

    return render(request, 'circuit/create.html', {'form': form})

####################################################################################################

@login_required
def details(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)
    return render(request, 'circuit/details.html', {'circuit': circuit})

####################################################################################################

@login_required
def update(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)

    if request.method == 'POST':
        form = CircuitForm(request.POST, instance=circuit)
        if form.is_valid():
            circuit = form.save()
            return HttpResponseRedirect(reverse('circuits.details', args=[circuit.pk]))
    else:
        form = CircuitForm(instance=circuit)

    return render(request, 'circuit/create.html', {'form': form, 'update': True, 'circuit': circuit})

####################################################################################################

@login_required
def boulders(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)

    # if request.method == 'POST':
    #     form = CircuitForm(request.POST, instance=circuit)
    #     if form.is_valid():
    #         circuit = form.save()
    #         return HttpResponseRedirect(reverse('circuits.details', args=[circuit.pk]))
    # else:
    # form = CircuitForm(instance=circuit)

    return render(request, 'circuit/boulders.html', {'circuit': circuit})

####################################################################################################

@login_required
def openers(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)

    person_data = [{'pk':person.pk, 'name':person.name} for person in Person.objects.all()] # last_first_
    person_data_json = json.dumps(person_data)

    return render(request, 'circuit/openers.html', {'circuit': circuit, 'person_data': person_data_json})

####################################################################################################

@login_required
def delete(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)
    messages.success(request, "Circuit «{0.name}» supprimé".format(circuit))
    circuit.delete()

    return HttpResponseRedirect(reverse('circuits.index'))

####################################################################################################
#
# End
#
####################################################################################################
