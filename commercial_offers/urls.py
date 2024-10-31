from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('commercial_offers/', views.commercial_offers_list, name='commercial_offers_list'),
    path('create_commercial_offer/', views.create_commercial_offer, name='create_commercial_offer'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit_commercial_offer/<int:pk>/', views.edit_commercial_offer, name='edit_commercial_offer'),
    path('generate_pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
    path('print_offer/<int:pk>/', views.print_offer, name='print_offer'),
    path('signup/', views.signup, name='signup'),
    path('products_list/', views.products_list, name='products_list'),
]