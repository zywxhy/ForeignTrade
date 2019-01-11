from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.views import View
from rest_framework.routers import SimpleRouter
from .serializer import BranchWarehousingModelSerializer
from .models import BranchWarehousing

# Create your views here.

class BranchWarehousingViewSet(ModelViewSet):
    serializer_class = BranchWarehousingModelSerializer
    queryset = BranchWarehousing.objects.all()


router = SimpleRouter()
router.register('branch_warehousing',BranchWarehousingViewSet)


class BranchWarehousingView(View):
    def get(self):
        pass