from django.urls import path, include
from . import views

app_name = 'accounts'  # This is why we use 'accounts:' prefix

urlpatterns = [
    # Login/Logout are handled by Django's default auth views,
    # but we include them here under the 'accounts' namespace.
    path('', include('django.contrib.auth.urls')),

    # Custom Views
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('address/add/', views.add_address, name='add_address'),
]