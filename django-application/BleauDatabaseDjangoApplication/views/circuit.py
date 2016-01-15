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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import ModelForm, Form, CharField
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

####################################################################################################

from ..models import Circuit

####################################################################################################

class CircuitForm(ModelForm):

    class Meta:
        model = Circuit
        fields = '__all__'
        # exclude = ('creation_date',)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(CircuitForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

# @login_required
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

# @login_required
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

# @login_required
def delete(request, circuit_id):

    # Fixme: confirmation
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    # Fixme: message not shown
    messages.success(request, "Circuit «{0.name}» supprimé".format(circuit))
    circuit.delete()

    return HttpResponseRedirect(reverse('circuits.index'))

####################################################################################################
#
# End
#
####################################################################################################
