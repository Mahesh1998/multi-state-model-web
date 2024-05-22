from django.shortcuts import render
from django.http import JsonResponse
from .models import Hamiltonian, Oligomer
import json
from rest_framework.decorators import api_view

# Create your views here.

def test_view(request):
    return JsonResponse({"key": "value"})

@api_view(['POST'])
def hamiltonian_compute(request):
    body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request.body)

    #Reformatting JSON input
    request_body['n'] = int(request_body['n'])
    print(request_body)
    request_body['couplings'] = list(request_body['couplings'])
    print(request_body)
    request_body['x'] = int(request_body['x'])


    print(request_body)


    Ham = Hamiltonian(n=5)
    Ham.set_couplings([-9.0,])
    Ham.shift_ends((-3.7, -3.7))

    Hs = Oligomer(n=5)
    Hs.set_H_system(Ham.H_system) # coupling matrix, reorganization not included
    Hs.solve()

    print(Hs)

    print(H)
    return JsonResponse(request_body)
