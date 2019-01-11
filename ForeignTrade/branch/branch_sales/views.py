from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import BranchSalesContractModelSerializer
from .models import BranchSalesContract
from rest_framework.routers import SimpleRouter
# Create your views here.


class SalesContractModelViewSet(ModelViewSet):

    serializer_class = BranchSalesContractModelSerializer
    pagination_class = None
    queryset = BranchSalesContract.objects.all()


router = SimpleRouter()
router.register('branch_warehousing',SalesContractModelViewSet)