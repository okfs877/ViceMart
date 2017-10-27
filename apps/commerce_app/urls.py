from django.conf.urls import url
from . import views




urlpatterns = [
    # url(r'^$', views.index),
    url(r'^shop$', views.index),
    url(r'^checkout$', views.checkout),
    url(r'^addproduct$', views.addproduct),
    url(r'^create$', views.create),
    url(r'^edit$', views.edit),
    url(r'^showCategory/(?P<category>.+)$', views.showCategory),
    url(r'^search$', views.search),
    url(r'^search/(?P<searchTerm>.+)$', views.showSearchResults),
    url(r'^search/$', views.index),
    url(r'^cart/(?P<id>\d+)$', views.cart),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^update/(?P<id>\d+)$', views.update),
]

