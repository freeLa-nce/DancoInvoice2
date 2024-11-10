from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_view, name='customer-view'),
    path('get_customer_list', views.get_customer_list, name="get-customer-list"),
    # path('add_customer', views.add_customer, name="add-customer"),
    # path('get_customer_by_id', views.get_customer_by_id, name="get-customer-by-id"),
    # path('edit_customer_by_id', views.edit_customer_by_id, name="edit-customer-by-id"),
    path('delete_customer_by_id', views.delete_customer_by_id, name="delete-customer-by-id"),
]
