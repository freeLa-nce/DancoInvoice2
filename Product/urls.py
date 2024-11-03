from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_view, name='product_view'),
    path('get_product_list', views.get_product_list, name="get_product_list"),
    path('add_product', views.add_product, name="add-product"),
    path('get_product_by_id', views.get_product_by_id, name="get-product-by-id"),
    path('edit_product_by_id', views.edit_product_by_id, name="edit-product-by-id"),
    path('delete_product_by_id', views.delete_product_by_id, name="delete-product-by-id"),
]
