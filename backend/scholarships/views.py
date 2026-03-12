from rest_framework import viewsets, permissions
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

# 4. LOGIKA BOOKMARK (Simpan Beasiswa)
class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated] # Harus login

    # Mahasiswa hanya bisa melihat bookmark miliknya sendiri
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    # Hanya Applicant yang boleh nge-bookmark, Admin tidak boleh
    def perform_create(self, serializer):
        if self.request.user.role != 'applicant':
            raise PermissionDenied("Hanya mahasiswa (applicant) yang bisa menyimpan beasiswa.")
        serializer.save(user=self.request.user)