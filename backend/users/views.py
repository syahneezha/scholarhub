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