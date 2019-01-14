from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import ClientModelSerializer,BranchClient
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class ClientModelViewSet(ModelViewSet):
    serializer_class = ClientModelSerializer
    queryset = BranchClient.objects.all()

