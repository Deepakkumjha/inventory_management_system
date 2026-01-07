from django.urls import path
from .views import item, single_product, get_pdf, get_excel

urlpatterns = [
    path('items/',item),
    path('items/<id>/',single_product),
    path('items/export/pdf/',get_pdf),
    path('items/export/excel/',get_excel)
]
