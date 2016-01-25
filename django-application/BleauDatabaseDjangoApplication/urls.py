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
#
# Main page
#

# from .views.main import MainView

urlpatterns = [
    # url(r'^$', MainView.as_view(), name='index'),

    url(r'^$',
        TemplateView.as_view(template_name='main.html'),
        name='index'),

    url(r'^about$',
        TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^about-rest-api$',
        TemplateView.as_view(template_name='about-rest-api.html'),
        name='about-rest-api'),

    url(r'^mentions-legales$',
        TemplateView.as_view(template_name='mentions-legales.html'),
        name='mentions-legales'),
]

####################################################################################################
#
# Authentication
#

import django.contrib.auth.views as auth_views

from .views.account import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .views import account as account_views

urlpatterns += [
   url(r'^account/login/$',
       auth_views.login,
       {'template_name': 'account/login.html',
        'authentication_form': AuthenticationForm},
       name='account.login'),

    url(r'^account/logout/$',
        auth_views.logout,
        {'template_name': 'account/logged_out.html'},
        name='account.logout'),

    url(r'^account/password/change/$',
        auth_views.password_change,
        {'template_name': 'account/password_change.html',
         'password_change_form': PasswordChangeForm,
         'post_change_redirect': reverse_lazy('account.password_change_done')},
        name='account.password_change'),

    url(r'^account/password/change/done/$',
        account_views.password_change_done,
        name='account.password_change_done'),

    url(r'^account/password/reset/$',
        auth_views.password_reset,
        {'template_name': 'account/password_reset.html',
         'email_template_name': 'account/password_reset_email.html',
         'password_reset_form': PasswordResetForm,
         'post_reset_redirect': reverse_lazy('account.password_reset_done')},
        name='account.password_reset'),

    url(r'^account/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'account/password_reset_confirm.html',
         'set_password_form': SetPasswordForm},
        name='account.password_reset_confirm'),

    url(r'^account/password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'account/password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^account/password/reset/done/$',
        account_views.password_reset_done,
        name='account.password_reset_done'),

    url(r'^account/profile/$',
        account_views.profile,
        name='account.profile'),

    url(r'^account/profile/update/$',
        account_views.update,
        name='account.profile.update'),

    url(r'^account/delete/$',
        account_views.delete,
        name='account.delete'),
]

####################################################################################################
#
# Person
#

from .views import person as person_views

urlpatterns += [
    url(r'^person/$',
        login_required(person_views.PersonListView.as_view()),
        name='person.index'),

    url(r'^person/(?P<person_id>\d+)/$',
        person_views.details,
        name='person.details'),

    url(r'^person/create/$',
        person_views.create,
        name='person.create'),

    url(r'^person/(?P<person_id>\d+)/update/$',
        person_views.update,
        name='person.update'),

    url(r'^person/(?P<person_id>\d+)/delete/$',
        person_views.delete,
        name='person.delete'),
]

####################################################################################################
#
# Place
#

from .views import place as place_views

urlpatterns += [
    url(r'^place/$',
        login_required(place_views.PlaceListView.as_view()),
        name='place.index'),

    url(r'^place/(?P<place_id>\d+)/$',
        place_views.details,
        name='place.details'),

    url(r'^place/create/$',
        place_views.create,
        name='place.create'),

    url(r'^place/(?P<place_id>\d+)/update/$',
        place_views.update,
        name='place.update'),

    url(r'^place/(?P<place_id>\d+)/delete/$',
        place_views.delete,
        name='place.delete'),
]

####################################################################################################
#
# Massif
#

from .views import massif as massif_views

urlpatterns += [
    url(r'^massif/$',
        login_required(massif_views.MassifListView.as_view()),
        name='massif.index'),

    url(r'^massif/create/$',
        massif_views.create,
        name='massif.create'),

    url(r'^massif/(?P<massif_id>\d+)/$',
        massif_views.details,
        name='massif.details'),

    url(r'^massif/(?P<massif_id>\d+)/update/$',
        massif_views.update,
        name='massif.update'),

    url(r'^massif/(?P<massif_id>\d+)/delete/$',
        massif_views.delete,
        name='massif.delete'),
]

####################################################################################################
#
# Circuit
#

from .views import circuit as circuit_views

urlpatterns += [
    url(r'^circuit/create/$',
        circuit_views.create,
        name='circuit.create'),

    url(r'^circuit/(?P<circuit_id>\d+)/$',
        circuit_views.details,
        name='circuit.details'),

    url(r'^circuit/(?P<circuit_id>\d+)/update/$',
        circuit_views.update,
        name='circuit.update'),

    url(r'^circuit/(?P<circuit_id>\d+)/boulder/$', # s?
        circuit_views.boulders,
        name='circuit.boulders'),

    url(r'^circuit/(?P<circuit_id>\d+)/opener/$',
        circuit_views.openers,
        name='circuit.openers'),

    url(r'^circuit/(?P<circuit_id>\d+)/delete/$',
        circuit_views.delete,
        name='circuit.delete'),
]

####################################################################################################
#
# Refection
#

from .views import refection as refection_views

urlpatterns += [
    url(r'^refection/create/$', # Fixme: (?P<circuit_id>\d+)
        refection_views.create,
        name='refection.create'),

    url(r'^refection/(?P<refection_id>\d+)/$',
        refection_views.details,
        name='refection.details'),

    url(r'^refection/(?P<refection_id>\d+)/update/$',
        refection_views.update,
        name='refection.update'),

    url(r'^refection/(?P<refection_id>\d+)/persons/$',
        refection_views.persons,
        name='refection.persons'),

    url(r'^refection/(?P<refection_id>\d+)/delete/$',
        refection_views.delete,
        name='refection.delete'),
]

####################################################################################################
#
# REST
#

from .views.rest import (PersonViewSet, PlaceViewSet,
                         MassifViewSet,
                         CircuitViewSet, RefectionViewSet)

router = routers.DefaultRouter()
router.register(r'circuit', CircuitViewSet)
router.register(r'massif', MassifViewSet)
router.register(r'person', PersonViewSet)
router.register(r'place', PlaceViewSet)
router.register(r'refection', RefectionViewSet)

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
