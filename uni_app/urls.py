from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('universities', views.UniversityViewSet)
router.register('courses', views.CourseViewSet)
router.register('university-courses', views.UniversityCourseViewSet)

urlpatterns = [
    path('', include(router.urls))
]