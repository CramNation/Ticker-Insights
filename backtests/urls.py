from django.urls import path

from . import views

urlpatterns = [
    path('earnings', views.index, name='earnings'),
    path('yieldcurve', views.yieldcurve, name='yieldcurve'),
    path('sma', views.sma,name='sma' ),

]