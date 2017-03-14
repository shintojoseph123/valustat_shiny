from django.contrib import admin
from django.conf.urls import url
from shiny import views

urlpatterns = [

    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^plotly_ajax/(?P<n>\d+)/$', views.plotly_ajax, name='plotly_ajax'),
    url(r'^plotly_ajax/$',views.plotly_ajax, name='plotly_ajax'),


]
