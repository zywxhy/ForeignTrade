from django.urls import path
from .views import BranchWarehousingView,BranchWarehousingListView,BranchWarehousingReviewView


urlpatterns = [
    path('branch_warehousing/operations',BranchWarehousingView.as_view(),name='branch_warehousing'),
    path('branch_warehousing/list',BranchWarehousingListView.as_view(),name='branch_warehousing_list'),
    path('warehousing_review/',BranchWarehousingReviewView.as_view(),name='warehousing_review')
]