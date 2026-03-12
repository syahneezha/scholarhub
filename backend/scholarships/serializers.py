from rest_framework import serializers
from .models import Category, Scholarship, Bookmark

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    # Ini agar API menampilkan nama kategori dan nama pembuat, bukan sekadar ID acak (UUID)
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('created_by',) # Admin tidak perlu mengisi ini, otomatis terisi oleh sistem

class BookmarkSerializer(serializers.ModelSerializer):
    scholarship_title = serializers.ReadOnlyField(source='scholarship.title')

    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = ('user',) # Otomatis terisi nama mahasiswa yang sedang login