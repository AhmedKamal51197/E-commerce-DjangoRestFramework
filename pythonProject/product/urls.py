from django.urls import path
from .views import *
urlpatterns=[
    path('products/',get_all_products,name='products'),
    path('products/<str:pk>/',get_Product_By_Id,name='get_product_by_id')
]