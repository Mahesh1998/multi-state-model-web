from django.urls import path
from . import views

urlpatterns = [
    path('hcompute', views.hamiltonian_compute, name="Hamiltonian Compute"),
]

