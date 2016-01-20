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

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

from rest_framework import routers

####################################################################################################

from .views.account import (AuthenticationForm,
                            PasswordChangeForm,
                            PasswordResetForm,
                            SetPasswordForm)

from .views.main import MainView

####################################################################################################
#
# Main page
#

urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),
    # url(r'^$',
    #     TemplateView.as_view(template_name='main.html'),
    #     name='index'),
    url(r'^mentions-legales$',
        TemplateView.as_view(template_name='mentions-legales.html'),
        name='mentions-legales'),
]

####################################################################################################
#
# Authentication
#

import django.contrib.auth.views as auth_views

urlpatterns += [
   url(r'^accounts/login/$',
       auth_views.login,
       {'template_name': 'account/login.html',
        'authentication_form': AuthenticationForm},
       name='accounts.login'), # Fixme: redirect to home page

    url(r'^accounts/logout/$',
        auth_views.logout,
        {'template_name': 'account/logged_out.html'},
        name='accounts.logout'),

    url(r'^accounts/password/change/$',
        auth_views.password_change,
        {'template_name': 'account/password_change.html',
         'password_change_form': PasswordChangeForm,
         'post_change_redirect': reverse_lazy('accounts.password_change_done')},
        name='accounts.password_change'),

    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        {'template_name': 'account/password_reset.html',
         'email_template_name': 'account/password_reset_email.html',
         'password_reset_form': PasswordResetForm,
         'post_reset_redirect': reverse_lazy('accounts.password_reset_done')},
        name='accounts.password_reset'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'account/password_reset_confirm.html',
         'set_password_form': SetPasswordForm},
        name='accounts.password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'account/password_reset_complete.html'},
        name='password_reset_complete'),
]

####################################################################################################
#
# Profile
#

from .views import account as account_views

urlpatterns += [
    url(r'^accounts/profile/$',
        account_views.profile,
        name='accounts.profile'),

    url(r'^accounts/profile/update/$',
        account_views.update,
        name='accounts.profile.update'),

    url(r'^accounts/password/change/done/$',
        account_views.password_change_done,
        name='accounts.password_change_done'),

    url(r'^accounts/password/reset/done/$',
        account_views.password_reset_done,
        name='accounts.password_reset_done'),

    url(r'^accounts/delete/$',
        account_views.delete,
        name='accounts.delete'),
]

####################################################################################################
#
# Person
#

from .views import person as person_views

urlpatterns += [
    url(r'^persons/$',
        login_required(person_views.PersonListView.as_view()),
        name='persons.index'),

    url(r'^persons/(?P<person_id>\d+)/$',
        person_views.details,
        name='persons.details'),

    url(r'^persons/create/$',
        person_views.create,
        name='persons.create'),

    url(r'^persons/(?P<person_id>\d+)/update/$',
        person_views.update,
        name='persons.update'),

    url(r'^persons/(?P<person_id>\d+)/delete/$',
        person_views.delete,
        name='persons.delete'),
]

####################################################################################################
#
# Place
#

from .views import place as place_views

urlpatterns += [
    url(r'^places/$',
        login_required(place_views.PlaceListView.as_view()),
        name='places.index'),

    url(r'^places/(?P<place_id>\d+)/$',
        place_views.details,
        name='places.details'),

    url(r'^places/create/$',
        place_views.create,
        name='places.create'),

    url(r'^places/(?P<place_id>\d+)/update/$',
        place_views.update,
        name='places.update'),

    url(r'^places/(?P<place_id>\d+)/delete/$',
        place_views.delete,
        name='places.delete'),
]

####################################################################################################
#
# Massif
#

from .views import massif as massif_views

urlpatterns += [
    url(r'^massifs/$',
        login_required(massif_views.MassifListView.as_view()),
        name='massifs.index'),

    url(r'^massifs/create/$',
        massif_views.create,
        name='massifs.create'),

    url(r'^massifs/(?P<massif_id>\d+)/$',
        massif_views.details,
        name='massifs.details'),

    url(r'^massifs/(?P<massif_id>\d+)/update/$',
        massif_views.update,
        name='massifs.update'),

    url(r'^massifs/(?P<massif_id>\d+)/delete/$',
        massif_views.delete,
        name='massifs.delete'),
]

####################################################################################################
#
# Circuit
#

from .views import circuit as circuit_views

urlpatterns += [
    url(r'^circuits/create/$',
        circuit_views.create,
        name='circuits.create'),

    url(r'^circuits/(?P<circuit_id>\d+)/$',
        circuit_views.details,
        name='circuits.details'),

    url(r'^circuits/(?P<circuit_id>\d+)/update/$',
        circuit_views.update,
        name='circuits.update'),

    url(r'^circuits/(?P<circuit_id>\d+)/delete/$',
        circuit_views.delete,
        name='circuits.delete'),

    url(r'^circuits/(?P<circuit_id>\d+)/boulders/$',
        circuit_views.boulders,
        name='circuits.boulders'),
]

####################################################################################################
#
# REST
#

from .views.rest import PersonViewSet, OpenerViewSet, PlaceViewSet, MassifViewSet, CircuitViewSet

router = routers.DefaultRouter()
router.register(r'place', PlaceViewSet)
router.register(r'massif', MassifViewSet)
router.register(r'circuit', CircuitViewSet)
router.register(r'person', PersonViewSet)
router.register(r'opener', OpenerViewSet)

urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
]

####################################################################################################
#
# End
#
####################################################################################################
