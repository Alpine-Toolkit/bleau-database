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

from ..models import Person

####################################################################################################

class PersonForm(ModelForm):

    class Meta:
        model = Person
        fields = '__all__'
        # exclude = ('creation_date',)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(PersonForm, self).__init__(*args, **kwargs)

        # self.fields['last_name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class PersonSearchForm(Form):

    name = CharField(label=_('Nom'), required=False, initial='')

    ##############################################

    def filter_by(self):
        return {'last_name__icontains': self.cleaned_data['name']}

####################################################################################################

class PersonListView(FormMixin, ListView):

    template_name = 'person/index.html'

    # ListView
    model = Person
    queryset = Person.objects.all().order_by('last_name')
    context_object_name = 'persons' # else object_list
    paginate_by = None

    # FormMixin
    form_class = PersonSearchForm

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
def details(request, person_id):

    person = get_object_or_404(Person, pk=person_id)

    # deprecated ?
    # return render_to_response('person/details.html',
    #                           {'person': person},
    #                           context_instance=RequestContext(request))
    return render(request, 'person/details.html', {'person': person})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            messages.success(request, "Person créé avec succès.")
            return HttpResponseRedirect(reverse('persons.details', args=[person.pk]))
        else:
            messages.error(request, "Des informations sont manquantes ou incorrectes")
    else:
        form = PersonForm()

    return render(request, 'person/create.html', {'form': form})

####################################################################################################

@login_required
def update(request, person_id):

    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save()
            return HttpResponseRedirect(reverse('persons.details', args=[person.pk]))
    else:
        form = PersonForm(instance=person)

    return render(request, 'person/create.html', {'form': form, 'update': True, 'person': person})

####################################################################################################

@login_required
def delete(request, person_id):

    # Fixme: confirmation
    person = get_object_or_404(Person, pk=person_id)
    messages.success(request, "Person «{0.name}» supprimé".format(person))
    person.delete()

    return HttpResponseRedirect(reverse('persons.index'))

####################################################################################################
#
# End
#
####################################################################################################
