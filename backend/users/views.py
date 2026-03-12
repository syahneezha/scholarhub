from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer
from .models import AuditLog, CustomUser

# --- 1. FUNGSI LIHAT PROFIL ---
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_my_profile(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "role": user.role 
    })

# --- 2. FUNGSI REGISTRASI (Dengan Log) ---
@api_view(['POST'])
@permission_classes([]) 
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # MATA-MATA BEKERJA: Catat Pendaftaran
        AuditLog.objects.create(
            user=user, 
            action="REGISTER_SUCCESS", 
            details=f"User baru mendaftar: {user.username}"
        )
        return Response({"message": "Berhasil daftar! Silakan login."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 3. FUNGSI LOGIN CUSTOM (Dengan Log) ---
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
        
        try:
            # Biarkan sistem JWT memvalidasi password
            response = super().post(request, *args, **kwargs)
            
            # Jika sukses melewati baris di atas, berarti password benar!
            user = CustomUser.objects.get(username=username)
            AuditLog.objects.create(
                user=user, action="LOGIN_SUCCESS", ip_address=ip, details="Berhasil login via API"
            )
            return response
            
        except Exception as e:
            # Jika password salah atau username tidak ada
            AuditLog.objects.create(
                user=None, action="LOGIN_FAILED", ip_address=ip, details=f"Gagal login untuk: {username}"
            )
            raise e
        

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

@api_view(['PUT']) # Gunakan PUT untuk update data
@permission_classes([IsAuthenticated]) # Hanya user login yang bisa update
@parser_classes([MultiPartParser, FormParser]) # Wajib ada ini agar API bisa menerima file (gambar)
def update_profile_picture(request):
    user = request.user

    # Cek apakah ada file yang dikirim dengan nama 'profile_picture'
    if 'profile_picture' not in request.FILES:
        return Response({'error': 'Tidak ada gambar yang diupload.'}, status=status.HTTP_400_BAD_REQUEST)

    # Simpan gambar ke database
    user.profile_picture = request.FILES['profile_picture']
    user.save()

    # Kembalikan URL gambar yang baru
    return Response({
        'message': 'Foto profil berhasil diperbarui!',
        'profile_picture_url': request.build_absolute_uri(user.profile_picture.url)
    }, status=status.HTTP_200_OK)