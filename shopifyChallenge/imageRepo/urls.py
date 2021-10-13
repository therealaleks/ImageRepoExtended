from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'image', views.imageViewSet)
router.register(r'imageSearch', views.imageSearchViewSet)
router.register(r'directory', views.directoryViewSet)
router.register(r'video', views.videoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]