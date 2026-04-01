from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

from .serializers import UserRegistrationSerializer
from .models import AuditLog, CustomUser

# --- 1. LIHAT PROFIL (GET) ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        # Jika ada foto profil, kirim URL-nya
        "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
    })

# --- 2. UPDATE NAMA/USER DATA (PATCH) ---
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    user = request.user
    new_username = request.data.get('username')
    
    if new_username:
        user.username = new_username
        user.save()
        
        # MATA-MATA (Audit Log): Catat perubahan nama
        AuditLog.objects.create(
            user=user,
            action="UPDATE_PROFILE",
            details=f"User mengganti nama menjadi: {new_username}"
        )
        return Response({"message": "Nama berhasil diperbarui!", "username": user.username})
    
    return Response({"error": "Data tidak valid"}, status=status.HTTP_400_BAD_REQUEST)

# --- 3. GANTI PASSWORD (POST) ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    
    if not new_password or len(new_password) < 8:
        return Response({"error": "Password minimal 8 karakter!"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Hash password (KEAMANAN: Jangan simpan teks asli!)
    user.password = make_password(new_password)
    user.save()
    
    AuditLog.objects.create(
        user=user,
        action="CHANGE_PASSWORD",
        details="User berhasil mengganti password"
    )
    return Response({"message": "Password berhasil diganti!"})

# --- 4. REGISTRASI ---
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        AuditLog.objects.create(
            user=user, 
            action="REGISTER_SUCCESS", 
            details=f"User baru terdaftar: {user.username}"
        )
        return Response({"message": "Berhasil daftar! Silakan login."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 5. LOGIN DENGAN LOGGING ---
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
        
        try:
            response = super().post(request, *args, **kwargs)
            user = CustomUser.objects.get(username=username)
            AuditLog.objects.create(
                user=user, action="LOGIN_SUCCESS", ip_address=ip, details="Berhasil masuk"
            )
            return response
        except Exception:
            AuditLog.objects.create(
                user=None, action="LOGIN_FAILED", ip_address=ip, details=f"Gagal login: {username}"
            )
            return Response({"detail": "Username atau password salah!"}, status=status.HTTP_401_UNAUTHORIZED)

# --- 6. UPDATE FOTO PROFIL ---
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile_picture(request):
    user = request.user
    if 'profile_picture' not in request.FILES:
        return Response({'error': 'Tidak ada gambar!'}, status=status.HTTP_400_BAD_REQUEST)

    user.profile_picture = request.FILES['profile_picture']
    user.save()
    return Response({
        'message': 'Foto profil diperbarui!',
        'profile_picture_url': request.build_absolute_uri(user.profile_picture.url)
    })