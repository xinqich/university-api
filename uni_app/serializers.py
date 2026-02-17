from rest_framework import serializers
from .models import University, Course, UniversityCourse


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"
        read_only_fields = ['id']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['id']

class UniversityCourseReadSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UniversityCourse
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks",
        ]

class UniversityCourseWriteSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all()
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    class Meta:
        model = UniversityCourse
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks",
        ]