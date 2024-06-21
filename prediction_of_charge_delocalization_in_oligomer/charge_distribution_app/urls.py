from django.urls import path
from . import views

urlpatterns = [
    path('ocompute', views.oligomer_compute, name="Oligomer Compute"),
    path('series/ocompute', views.series_oligomer_compute, name="Series Oligomer Compute"),
    path('', views.home, name="Home Page"),
]

