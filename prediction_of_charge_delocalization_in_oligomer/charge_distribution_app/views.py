from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings as django_settings
from .models import Hamiltonian, Oligomer
import json
from rest_framework.decorators import api_view
from matplotlib import pyplot as plt
import os
import numpy as np

# Create your views here.

def home(request):
    return render(request=request, template_name="home.html") 

@api_view(['POST'])
def oligomer_compute(request):
    print(request)
    body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request.body)

    #Reformatting JSON input
    request_body['n'] = int(request_body['n'])
    request_body['couplings'] = [eval(i) for i in request_body['couplings']]
    request_body['shift_ends'] = [eval(i) for i in request_body['shift_ends']]

    Ham = Hamiltonian(n=request_body['n'])
    Ham.set_couplings(request_body['couplings'])
    Ham.shift_ends(request_body['shift_ends'])

    Hs = Oligomer(n=request_body['n'])
    Hs.set_H_system(Ham.H_system) # coupling matrix, reorganization not included
    Hs.solve()
    print(Hs[Hs.global_minimum(1)[0]].get_charges(1))
    plt.bar(["c1","c2","c3","c4", "c5"], Hs[Hs.global_minimum(1)[0]].get_charges(1))

    if not os.path.exists(django_settings.STATIC_IMAGES):
        os.makedirs(django_settings.STATIC_IMAGES)
    

    print(os.path.join(django_settings.STATIC_IMAGES, "bar.jpg"))
    plt.savefig(os.path.join(django_settings.STATIC_IMAGES, "bar.jpg"))
    plt.close()

    json_response = Hs.json_output()

    json_response['barplot'] = "images/bar.jpg"


    return JsonResponse(json_response)


@api_view(['POST'])
def series_oligomer_compute(request):
    body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request.body)
    print(request_body)

    request_body['n_low'] = int(request_body['n_low'])
    request_body['n_high'] = int(request_body['n_high'])
    request_body['couplings'] = [eval(i) for i in request_body['couplings']]
    request_body['shift_ends'] = [eval(i) for i in request_body['shift_ends']]

    oligomers_n = range(request_body['n_low'], request_body['n_high'])
    oligomers = []

    for n in oligomers_n:
        Ham = Hamiltonian(n=n)
        Ham.set_couplings([-9.0,])
        Ham.shift_ends((-3.7, -3.7))

        Hs = Oligomer(n=n)
        Hs.set_H_system(Ham.H_system)
        Hs.solve()

        oligomers.append(Hs)
    
    if not os.path.exists(django_settings.STATIC_IMAGES):
        os.makedirs(django_settings.STATIC_IMAGES)
    

    # make a plot of the ground state energy vs x
    for i, oligomer in enumerate(oligomers):
        plt.plot(oligomer.xrange - oligomer.xrange.mean(), oligomer.get_state_curve(1), label=f'{oligomers_n[i]}')
    plt.savefig(os.path.join(django_settings.STATIC_IMAGES, "ground_state.jpg"))
    plt.close()
    
    # make a plot of global_min energy vs 1/n
    global_min = np.array([oligomer.global_minimum(1)[2] for oligomer in oligomers])
    plt.plot(1 / np.array(oligomers_n), global_min, 'o-', c="skyblue")
    plt.savefig(os.path.join(django_settings.STATIC_IMAGES, "golbal_minimum.jpg"))
    plt.close()


    return JsonResponse({"status": "success", 
                        "global_min_plot": "images/golbal_minimum.jpg",
                        "ground_state_plot": "images/ground_state.jpg"})

