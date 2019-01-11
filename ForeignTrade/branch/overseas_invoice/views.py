from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import SimpleRouter
from .models import OverseasInvoice
from .serializer import OverseasInvoiceModelSerializer

# Create your views here.

class OverseasInvoiceModelViewSet(ModelViewSet):
    queryset = OverseasInvoice.objects.all()
    serializer_class = OverseasInvoiceModelSerializer
    pagination_class = None



router = SimpleRouter()
router.register('overseas_invoice/api',OverseasInvoiceModelViewSet)