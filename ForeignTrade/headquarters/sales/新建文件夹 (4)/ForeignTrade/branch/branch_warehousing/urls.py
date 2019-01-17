from django.urls import path
from .views import BranchWarehousingView


urlpatterns = [
    path('branch_warehousing/operations',BranchWarehousingView.as_view(),name='branch_warehousing')
]