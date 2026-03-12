from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

# Semua import dari users.views digabung di satu baris ini
from users.views import get_my_profile, register_user, CustomLoginView, update_profile_picture

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTH & PROFIL ---
    path('api/register/', register_user, name='register'),
    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', get_my_profile, name='my_profile'),
    
    # Pintu upload foto (dimasukkan ke DALAM urlpatterns)
    path('api/profile/upload-foto/', update_profile_picture, name='upload_foto'),
    
    # --- MANAJEMEN BEASISWA ---
    path('api/', include('scholarships.urls')),
]

# --- PENGATURAN MEDIA/FOTO ---
# Agar foto bisa diakses lewat URL browser
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)