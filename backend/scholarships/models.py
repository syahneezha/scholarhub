import uuid
from django.db import models
from django.conf import settings

# 1. TABEL KATEGORI (Contoh: Prestasi, Kurang Mampu)
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. TABEL BEASISWA (Pusat Data Utama)
# 2. TABEL BEASISWA (Pusat Data Utama)
class Scholarship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255) 
    description = models.TextField()
    
    # --- TAMBAHKAN BARIS INI UNTUK POSTER ---
    poster = models.ImageField(upload_to='scholarship_posters/', null=True, blank=True)
    # ----------------------------------------
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='scholarships')
    quota = models.IntegerField(default=0)
    deadline = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_scholarships')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# 3. TABEL BOOKMARK (Fitur Simpanan Mahasiswa)
class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relasi: Siapa Mahasiswanya & Beasiswa mana yang disimpan
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='bookmarked_by')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Aturan unik: Satu mahasiswa tidak bisa mem-bookmark beasiswa yang sama 2 kali
        unique_together = ('user', 'scholarship') 

    def __str__(self):
        return f"{self.user.username} menyimpan {self.scholarship.title}"