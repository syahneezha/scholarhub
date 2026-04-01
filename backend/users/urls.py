from django.urls import path
from . import views

urlpatterns = [
    # Alamat untuk ambil data profil (Nama & Email)
    path('me/', views.get_my_profile, name='get_profile'),
    
    # Alamat untuk update nama
    path('update/', views.update_my_profile, name='update_profile'),
    
    # Alamat untuk ganti password
    path('change-password/', views.change_password, name='change_password'),
    
    # Alamat registrasi
    path('register/', views.register_user, name='register'),
    
    # Alamat login (Menggunakan class CustomLoginView kamu)
    path('login/', views.CustomLoginView.as_view(), name='login'),
]