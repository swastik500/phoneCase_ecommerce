from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('manager/', views.owner_dashboard, name='owner_dashboard'),
    path('manager/order/<int:order_id>/', views.process_order, name='process_order'),
]