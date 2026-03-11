from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Buat password write_only agar tidak pernah ditampilkan kembali saat API membalas
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Gunakan create_user agar password otomatis di-hashing (di-enkripsi pakai Argon2)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='applicant' # Semua yang daftar lewat API publik otomatis jadi Applicant
        )
        return user