from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotation_view, name='quotation'),
    path('search-items/', views.search_items, name='search_items'),
    path('update-product-quantity/', views.update_product_quantity, name='update-product-quantity'),

]
