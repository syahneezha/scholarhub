from rest_framework import serializers
from .models import Category, Scholarship, Bookmark

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    # Tambahkan ini agar URL gambar lengkap (http://localhost:8000/media/...)
    poster = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('created_by',)
        
class BookmarkSerializer(serializers.ModelSerializer):
    scholarship_title = serializers.ReadOnlyField(source='scholarship.title')

    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = ('user',) # Otomatis terisi nama mahasiswa yang sedang login