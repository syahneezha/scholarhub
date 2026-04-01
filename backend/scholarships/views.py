from rest_framework.response import Response  # Tambahkan ini
from rest_framework import status             # Dan inifrom rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Category, Scholarship, Bookmark
from .serializers import CategorySerializer, ScholarshipSerializer, BookmarkSerializer

# 1. ATURAN KUSTOM: Hanya Admin yang boleh merubah data (Write), selain itu cuma boleh melihat (Read)
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # Jika cuma GET (melihat)
            return True
        # Jika POST/PUT/DELETE, pastikan dia sudah login dan role-nya admin
        return request.user.is_authenticated and request.user.role == 'admin'

# 2. LOGIKA KATEGORI
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

# 3. LOGIKA BEASISWA
class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Saat Admin membuat beasiswa baru, otomatis catat siapa pembuatnya
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# scholarships/views.py

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 1. Ambil ID beasiswa dari request
        scholarship_id = request.data.get('scholarship')
        
        # 2. Cek apakah user ini sudah pernah simpan beasiswa ini?
        exists = Bookmark.objects.filter(user=request.user, scholarship_id=scholarship_id).exists()
        
        if exists:
            # Jika sudah ada, kirim pesan ramah, jangan ERROR 500
            return Response(
                {"detail": "Beasiswa ini sudah ada di daftar simpanan kamu!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 3. Jika belum ada, jalankan proses simpan seperti biasa
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)