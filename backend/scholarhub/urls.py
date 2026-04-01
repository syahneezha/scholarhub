from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

# Import semua fungsi dari users.views
from users.views import (
    get_my_profile, 
    register_user, 
    CustomLoginView, 
    update_profile_picture,
    update_my_profile,  # Tambahkan ini
    change_password     # Tambahkan ini
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTH & PROFIL ---
    path('api/register/', register_user, name='register'),
    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Alamat yang dipanggil oleh profile.html
    path('api/users/me/', get_my_profile, name='my_profile'), 
    path('api/users/update/', update_my_profile, name='update_profile'),
    path('api/users/change-password/', change_password, name='change_password'),
    
    # Pintu upload foto
    path('api/profile/upload-foto/', update_profile_picture, name='upload_foto'),
    
    # --- MANAJEMEN BEASISWA ---
    path('api/', include('scholarships.urls')),
]

# --- PENGATURAN MEDIA/FOTO ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)