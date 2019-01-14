from django.urls import path
from .views import BranchWarehousingView,BranchWarehousingListView


urlpatterns = [
    path('branch_warehousing/operations',BranchWarehousingView.as_view(),name='branch_warehousing'),
    path('branch_warehousing/list',BranchWarehousingListView.as_view(),name='branch_warehousing_list')

]