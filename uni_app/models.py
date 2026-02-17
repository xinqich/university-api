from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<University(pk={self.pk!r}, name={self.name!r})>"


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Course(pk={self.pk!r}, title={self.title!r})>"


class UniversityCourse(models.Model):
    university = models.ForeignKey(University, related_name="courses_offered", on_delete=models.PROTECT)
    course = models.ForeignKey(Course, related_name="universities_offering", on_delete=models.PROTECT)
    semester = models.CharField(max_length=50)
    duration_weeks = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "University Course"
        verbose_name_plural = "University Courses"
        constraints = [
            models.UniqueConstraint(fields=["course", "university", "semester"], name="unique_course_per_semester_per_university")
        ]

    def __str__(self):
        return f"{self.university.name} — {self.course.title} ({self.semester})"

    def __repr__(self):
        return f"<UniversityCourse(pk={self.pk!r}, university_id={self.university_id!r}, course_id={self.course_id!r}, semester={self.semester!r})>"
