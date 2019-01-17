from django.urls import path
from django.views.generic.base import TemplateView
from users.views import *

urlpatterns = [
    path('test/',A,name='test'),
    path('refresh_captcha/',refresh_captcha,name='refresh_captcha',),
    path('666/',FormView.as_view(),name='666'),

]