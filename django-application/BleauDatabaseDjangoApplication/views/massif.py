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
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

####################################################################################################

from ..models import Massif

####################################################################################################

class MassifForm(ModelForm):

    class Meta:
        model = Massif
        fields = '__all__'
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

    model = Massif
    template_name = 'massif/index.html'
    context_object_name = 'massifs'
    queryset = Massif.objects.all().order_by('name')
    paginate_by = 25
    form_class = MassifSearchForm

    ##############################################

    def get_form_kwargs(self):
        # Called by self.get_form
        return {'initial': self.get_initial(),
                'prefix': self.get_prefix(),
                'data': self.request.GET or None}

    ##############################################

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object_list = self.object_list.filter(**form.filter_by())
            name_query = form.cleaned_data['name']
            query = '&name=' + name_query # Fixme: escape
        else:
            query = ''

        # allow_empty = self.get_allow_empty() # assumed to be True
        context = self.get_context_data(form=form, query=query)
        return self.render_to_response(context)

####################################################################################################
#
# End
#
####################################################################################################
