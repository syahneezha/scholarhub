from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AuditLog

# 1. Mengatur Tampilan Tabel User
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Kolom apa saja yang mau ditampilkan di tabel depan
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # Fitur pencarian dan filter
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

    # Menambahkan field 'role' dan 'profile_picture' ke form edit admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Tambahan (PBL)', {'fields': ('role', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Tambahan (PBL)', {'fields': ('role', 'profile_picture')}),
    )

# 2. Mengatur Tampilan Tabel Audit Log (Mata-mata)
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'ip_address')
    
    # SECURITY FEATURE: Mengunci tabel agar tidak bisa diedit/ditambah dari admin panel
    readonly_fields = ('user', 'action', 'ip_address', 'timestamp', 'details')

    def has_add_permission(self, request):
        return False # Tidak bisa tambah log manual

    def has_change_permission(self, request, obj=None):
        return False # Tidak bisa edit log

    def has_delete_permission(self, request, obj=None):
        # Opsional: Ubah jadi False kalau log tidak boleh dihapus sama sekali
        return True