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

from ..models import Place

####################################################################################################

class PlaceForm(ModelForm):

    class Meta:
        model = Place
        fields = '__all__'
        # exclude = ('creation_date',)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(PlaceForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class PlaceSearchForm(Form):

    name = CharField(label=_('Nom'), required=False, initial='')

    ##############################################

    def filter_by(self):
        return {'name__icontains': self.cleaned_data['name']}

####################################################################################################

class PlaceListView(FormMixin, ListView):

    template_name = 'place/index.html'

    # ListView
    model = Place
    queryset = Place.objects.all().order_by('name')
    context_object_name = 'places' # else object_list
    paginate_by = None

    # FormMixin
    form_class = PlaceSearchForm

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
def details(request, place_id):

    place = get_object_or_404(Place, pk=place_id)
    return render(request, 'place/details.html', {'place': place})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.save()
            messages.success(request, "Place créé avec succès.")
            return HttpResponseRedirect(reverse('places.details', args=[place.pk]))
        else:
            messages.error(request, "Des informations sont manquantes ou incorrectes")
    else:
        form = PlaceForm()

    return render(request, 'place/create.html', {'form': form})

####################################################################################################

@login_required
def update(request, place_id):

    place = get_object_or_404(Place, pk=place_id)

    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            place = form.save()
            return HttpResponseRedirect(reverse('places.details', args=[place.pk]))
    else:
        form = PlaceForm(instance=place)

    return render(request, 'place/create.html', {'form': form, 'update': True, 'place': place})

####################################################################################################

@login_required
def delete(request, place_id):

    place = get_object_or_404(Place, pk=place_id)
    messages.success(request, "Place «{0.name}» supprimé".format(place))
    place.delete()

    return HttpResponseRedirect(reverse('places.index'))

####################################################################################################
#
# End
#
####################################################################################################
