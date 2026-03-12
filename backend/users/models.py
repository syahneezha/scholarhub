import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. CUSTOM USER MODEL (RBAC)
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('applicant', 'Applicant'),
    )
    # Menggunakan UUID agar ID user tidak mudah ditebak (Security Best Practice)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    email = models.EmailField(unique=True)

    # --- TAMBAHAN BARU UNTUK FOTO PROFIL ---
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # ---------------------------------------

    def __str__(self):
        return f"{self.username} ({self.role})"

# 2. AUDIT LOG MODEL (Tabel Mata-mata)
class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255) # Contoh: "LOGIN_SUCCESS", "DELETE_SCHOLARSHIP"
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'audit_logs' # NAMA TABEL INI HARUS SAMA PERSIS DENGAN YANG DI VAULT!
        
    def __str__(self):
        return f"[{self.timestamp}] {self.user} - {self.action}"