# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', P2PViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
