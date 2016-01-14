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
from django.views.generic import TemplateView
from rest_framework import routers

####################################################################################################

# from .views.main import MainView
from .views.rest import PlaceViewSet, MassifViewSet, CircuitViewSet

####################################################################################################
#
# Main page
#

urlpatterns = [
   # url(r'^$', MainView.as_view(), name='index'),
    url(r'^$',
        TemplateView.as_view(template_name='main.html'),
        name='index'),
    url(r'^mentions-legales$',
        TemplateView.as_view(template_name='mentions-legales.html'),
        name='mentions-legales'),
]

####################################################################################################
#
# Massif
#

from .views import massif as massif_views

urlpatterns += [
    url(r'^massifs/$',
        massif_views.MassifListView.as_view(),
        name='massifs.index'),

    # url(r'^massifs/create/$',
    #     massif_views.create,
    #     name='massifs.create'),

    # url(r'^massifs/(?P<massif_id>\d+)/$',
    #     # 'details',
    #     login_required(MassifCatalogListView.as_view()),
    #     name='massifs.details'),

    # url(r'^massifs/(?P<massif_id>\d+)/update/$',
    #     massif_views.update,
    #     name='massifs.update'),

    # url(r'^massifs/(?P<massif_id>\d+)/delete/$',
    #     massif_views.delete,
    #     name='massifs.delete'),
]

####################################################################################################
#
# REST
#

router = routers.DefaultRouter()
router.register(r'place', PlaceViewSet)
router.register(r'massif', MassifViewSet)
router.register(r'circuit', CircuitViewSet)

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
