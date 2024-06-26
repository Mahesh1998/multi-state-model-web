from django.shortcuts import render
from django.http import JsonResponse
#from django.conf import settings as django_settings
from .models import Hamiltonian, Oligomer
import json
from rest_framework.decorators import api_view
from matplotlib import pyplot as plt
import os
import numpy as np
from io import BytesIO
import base64 

# Create your views here.

def home(request):
    return render(request=request, template_name="home.html") 

def encode_image_to_base64(img_io):
    # Encode the image to Base64
    img_str = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return img_str

@api_view(['POST'])
def oligomer_compute(request):
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
    
    charge_dist = BytesIO()
    plt.xlabel("Monomer Unit")
    plt.ylabel("Charge")
    plt.title("Charge Distribution at Global Minimum")
    plt.savefig(charge_dist, format='png', dpi=600)
    plt.close()

    global_min_plot = BytesIO()
    plt.plot(Hs.xrange - Hs.xrange.mean(), Hs.get_state_curve(1))
    plt.xlabel("x")
    plt.ylabel("G/λ")
    plt.title("Free Energy Curve of Charge Transfer within oligomer")
    plt.savefig(global_min_plot, format='png', dpi=600)
    plt.close()
    

    json_response = Hs.json_output()

    json_response['charge_dist'] = encode_image_to_base64(charge_dist)

    json_response['global_min_plot'] = encode_image_to_base64(global_min_plot)


    return JsonResponse(json_response)


@api_view(['POST'])
def series_oligomer_compute(request):
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
    

    # make a plot of the ground state energy vs x
    for i, oligomer in enumerate(oligomers):
        plt.plot(oligomer.xrange - oligomer.xrange.mean(), oligomer.get_state_curve(1), label=f'{oligomers_n[i]}')
    
    plt.xlabel("x")
    plt.ylabel("G/λ")
    plt.title("Free Energy Curve of Charge Transfer within oligomer")
    
    global_min_plot =  BytesIO()
    plt.savefig(global_min_plot, format='png', dpi=600)
    plt.close()
    
    # make a plot of global_min energy vs 1/n
    global_min = np.array([oligomer.global_minimum(1)[2] for oligomer in oligomers])
    
    ground_state_plot =  BytesIO()
    plt.plot(1 / np.array(oligomers_n), global_min, 'o-', c="skyblue")
    plt.xlabel("1\n")
    plt.ylabel("G/λ")
    plt.title("Free energy of Polaron Stabilization energy")
    plt.savefig(ground_state_plot, format='png', dpi=600)
    plt.close()


    return JsonResponse({"status": "success", 
                        "global_min_plot": encode_image_to_base64(global_min_plot),
                        "ground_state_plot": encode_image_to_base64(ground_state_plot)})

