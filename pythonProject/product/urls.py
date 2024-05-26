from django.urls import path
from .views import *
urlpatterns=[
    path('products/',get_all_products,name='products'),
    path('products/<str:pk>/',get_Product_By_Id,name='get_product_by_id'),
    path('products/new',add_product,name='add_product'),
    path('products/update/<str:pk>/',update_product,name='update_product'),
    path('products/<str:product_id>/reviews/',create_review,name='create_review'),
    path('products/<str:product_id>/reviews/delete/',delete_review,name="delete_review"),
]