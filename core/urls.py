from django.urls import path
from .views import EHRConnectionViewSet, AuthViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("ehr",EHRConnectionViewSet,basename="ehr")
urlpatterns = router.urls
