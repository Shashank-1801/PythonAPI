from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pin/find$', views.find, name='find'),
    url(r'^pin/tags$', views.tags, name='tags'),
    url(r'^pin/generate_tags$', views.generate_tags, name='generate_tags'),
    url(r'^$', views.index, name='index'),

]