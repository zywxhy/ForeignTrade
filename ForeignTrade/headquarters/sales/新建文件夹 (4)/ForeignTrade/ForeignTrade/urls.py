"""ForeignTrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users.views import LoginView,LoginoutView,HomeView
from django.views.static import serve
from django.conf.urls.static import static
from ForeignTrade import settings
from django.conf.urls import url
import xadmin
from branch_client.urls import router as branch_client_url
from domestic_invoice.views import router as domestic_invoice_url
from sales.views import router as sales_url
from rest_framework.documentation import include_docs_urls
from branch_warehousing.views import router as bran_ware_url
from branch_sales.views import router as bran_sales_url



urlpatterns = [
    #url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('login/',LoginView.as_view(),name='login'),
    path('loginout/',LoginoutView.as_view(),name='loginout'),
    path('home/',HomeView.as_view(),name='home'),
    path('xadmin/', xadmin.site.urls),

    # rest_ramework
    path('auth_api/',include('rest_framework.urls')),
    url('docs/', include_docs_urls(title="润州ERP项目API文档")),


    path('users/' , include('users.urls')),
    path('sales/' , include('sales.urls')),
    path('purchase/' , include('purchase.urls')),
    path('product/' , include('product.urls')),
    path('captcha/', include('captcha.urls')),
    path('supplier/', include('supplier.urls')),
    path('client/', include('client.urls')),
    path('finance/', include('finance.urls')),
    path('stock/', include('stock.urls')),
    path('invoice/', include('invoice.urls')),
    path('storage/', include('storage.urls')),


    path('' , include('domestic_invoice.urls')),
    path('', include('overseas_invoice.urls')),
    path('', include('branch_sales.urls')),
    path('' , include('branch_warehousing.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += domestic_invoice_url.urls
urlpatterns += branch_client_url.urls
urlpatterns += sales_url.urls
urlpatterns += bran_ware_url.urls
urlpatterns += bran_sales_url.urls
