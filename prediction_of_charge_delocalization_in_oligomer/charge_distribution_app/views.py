from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings as django_settings
from .models import Hamiltonian, Oligomer
import json
from rest_framework.decorators import api_view
from matplotlib import pyplot as plt
import os

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
    print(os.path.join(django_settings.STATIC_ROOT,"bar.jpg"))
    plt.savefig(os.path.join(django_settings.STATIC_ROOT,"bar.jpg"))

    json_response = Hs.json_output()

    json_response['barplot'] = os.path.join(django_settings.STATIC_URL,"bar.jpg")


    return JsonResponse(json_response)
