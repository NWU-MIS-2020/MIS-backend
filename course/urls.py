from django.urls import path
from course.views import Courses, Grades, CourseStudents

urlpatterns = [
    path("courses/", Courses.as_view()),
    path("grades/", Grades.as_view()),
    path("course_students/", CourseStudents.as_view()),
]
