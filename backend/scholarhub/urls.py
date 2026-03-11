from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import get_my_profile, register_user, CustomLoginView # <-- Import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth & Profil
    path('api/register/', register_user, name='register'),
    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'), # <-- Gunakan CustomLoginView di sini
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', get_my_profile, name='my_profile'),
]