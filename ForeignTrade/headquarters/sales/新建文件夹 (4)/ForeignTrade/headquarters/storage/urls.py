from django.urls import path
from storage.views import StorageAddView,StorageModifyView,StorageDetailsView,StorageView

urlpatterns = [
    path('add/',StorageAddView.as_view(),name='storage_add'),
    path('modify/',StorageModifyView.as_view(),name='storage_modify'),
    path('details/',StorageDetailsView.as_view(),name='storage_details'),
    path('view/',StorageView.as_view(),name='storage_view'),
]


