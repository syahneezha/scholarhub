from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ScholarshipViewSet, BookmarkViewSet

# Router otomatis membuatkan alamat untuk CRUD (Create, Read, Update, Delete)
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]
