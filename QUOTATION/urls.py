from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotation_view, name='quotation'),
]
