
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-farmer/', views.add_farmer, name='add_farmer'),
    path('add-produce/', views.add_produce, name='add_produce'),
    path('add-order/', views.add_order, name='add_order'),
    path('match/<int:order_id>/', views.match_order, name='match_order'),
]
