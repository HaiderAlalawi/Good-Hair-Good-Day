"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from ninja import NinjaAPI 
from config import settings
from django.conf.urls.static import static

from pharmacy.apis.api_account import account_router
from pharmacy.apis.api_statistic import statistics_router
from pharmacy.apis.api_outcome import outcome_router
from pharmacy.apis.sign_in_api import sign_in_router
from pharmacy.apis.api_product import product_router
from pharmacy.apis.api_sale_item import sale_item_router



api=NinjaAPI()

api.add_router('signin', sign_in_router)
api.add_router('shopping_bill/', account_router)
api.add_router('sale_item/', sale_item_router)
api.add_router('outcome/', outcome_router)
api.add_router('statistics/', statistics_router)
api.add_router('item/', product_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('good-hair-good-day/',api.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]