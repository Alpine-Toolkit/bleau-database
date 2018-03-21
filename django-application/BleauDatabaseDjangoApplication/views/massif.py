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
from django.forms import ModelForm, Form, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

####################################################################################################

from ..models import Massif

####################################################################################################

class MassifForm(ModelForm):

    class Meta:
        model = Massif
        fields = (
            'name',
            'alternative_name',
            'sector',
            'chaos_type',
            'note',
            # 'coordinate',
            'parcelles',
            'access',
            'velo',
            'rdv',
        )

        # exclude = ('creation_date',)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(MassifForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class MassifSearchForm(Form):

    name = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        return {'name__icontains': self.cleaned_data['name']}

####################################################################################################

class MassifListView(FormMixin, ListView):

    template_name = 'massif/index.html'

    # ListView
    model = Massif
    queryset = Massif.objects.all().order_by('name')
    context_object_name = 'massifs' # else object_list
    paginate_by = None

    # FormMixin
    form_class = MassifSearchForm

    ##############################################

    def get_form_kwargs(self):

        # FormMixin: Build the keyword arguments required to instantiate the form.
        # cf. django/views/generic/edit.py FormMixin

        # Called by self.get_form
        kwargs = {'initial': self.get_initial(),
                  'prefix': self.get_prefix(),
                  'data': self.request.GET or None}
        # {'initial': {}, 'data': None, 'prefix': None}
        # {'data': <QueryDict: {'csrfmiddlewaretoken': ['KVIpPCTNju6cV6I6VvNaw0jfYFgF6t0u'], 'name': ['apr']}>, 'initial': {}, 'prefix': None}
        return kwargs

    ##############################################

    def get(self, request, *args, **kwargs):

        # cf. django/views/generic/list.py BaseListView

        self.object_list = self.get_queryset()

        form = self.get_form()
        if form.is_valid():
            self.object_list = self.object_list.filter(**form.filter_by())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

####################################################################################################

@login_required
def details(request, massif_id):

    massif = get_object_or_404(Massif, pk=massif_id)
    return render(request, 'massif/details.html', {'massif': massif})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = MassifForm(request.POST)
        if form.is_valid():
            massif = form.save(commit=False)
            massif.save()
            messages.success(request, _("Massif créé avec succès."))
            return HttpResponseRedirect(reverse('massif.details', args=[massif.pk]))
        else:
            messages.error(request, _("Des informations sont manquantes ou incorrectes"))
    else:
        form = MassifForm()

    return render(request, 'massif/create.html', {'form': form})

####################################################################################################

@login_required
def update(request, massif_id):

    massif = get_object_or_404(Massif, pk=massif_id)

    if request.method == 'POST':
        form = MassifForm(request.POST, instance=massif)
        if form.is_valid():
            massif = form.save()
            return HttpResponseRedirect(reverse('massif.details', args=[massif.pk]))
    else:
        form = MassifForm(instance=massif)

    return render(request, 'massif/create.html', {'form': form, 'update': True, 'massif': massif})

####################################################################################################

@login_required
def delete(request, massif_id):

    massif = get_object_or_404(Massif, pk=massif_id)
    messages.success(request, _("Massif «{0.name}» supprimé").format(massif))
    massif.delete()

    return HttpResponseRedirect(reverse('massif.index'))
