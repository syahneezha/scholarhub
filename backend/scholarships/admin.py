from django.contrib import admin
from .models import Category, Scholarship, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'quota', 'deadline', 'created_by')
    
    # Panel filter di sebelah kanan layar
    list_filter = ('category', 'deadline', 'provider')
    
    # Kolom pencarian di atas tabel
    search_fields = ('title', 'provider', 'description')
    
    # Fitur navigasi cepat berdasarkan tanggal
    date_hierarchy = 'deadline'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'scholarship', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'scholarship__title')
    
    # Mencegah edit bookmark, karena ini murni aktivitas sistem
    readonly_fields = ('user', 'scholarship', 'created_at')