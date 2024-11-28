from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_view, name='invoice-view'),
    path('generate-invoicenumber/', views.get_invoice_number, name='generate-invoice-number'),
    # path('update-product-quantity/', views.update_product_quantity, name='update-product-quantity'),
    path('save-invoice/', views.save_invoice, name='save-invoice'),
    path('edit_invoice/', views.edit_invoice, name='edit-invoice' )
    

]
