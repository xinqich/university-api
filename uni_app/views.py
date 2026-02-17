from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import University, Course, UniversityCourse
from .serializers import UniversitySerializer, CourseSerializer, UniversityCourseReadSerializer, UniversityCourseWriteSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class BaseNoUpdateViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

class UniversityViewSet(BaseNoUpdateViewSet):
    queryset = University.objects.all().distinct()
    serializer_class = UniversitySerializer

    @action(detail=True, url_path='courses', url_name='view-courses')
    def view_courses(self, request, pk=None):
        university = self.get_object()
        university_courses = university.courses_offered.all()
        serializer = UniversityCourseReadSerializer(university_courses, many=True)
        return Response(data=serializer.data)

    @action(detail=True, url_path='course-stats')
    def course_stats(self, request, pk=None):
        university = self.get_object()
        avg_duration = university.courses_offered.aggregate(avg_duration=Avg('duration_weeks'))
        data = {
            'total_courses': university.courses_offered.count(),
            'average_duration': avg_duration['avg_duration']
        }
        return Response(data)


class CourseViewSet(BaseNoUpdateViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class UniversityCourseViewSet(BaseNoUpdateViewSet):
    queryset = UniversityCourse.objects.order_by('id')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['university__name', 'course__title']
    ordering_fields = ['duration_weeks']
    filterset_fields = {
        "course__title": ['contains', 'icontains'],
        "semester": ['contains', 'icontains']
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return UniversityCourseWriteSerializer
        return UniversityCourseReadSerializer
