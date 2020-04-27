from django.urls import path
from course.views import Courses, Grades, CourseStudents, CMGrades, StudentsGrades

urlpatterns = [
    path("courses/", Courses.as_view()),
    path("grades/", Grades.as_view()),
    path("course_students/", CourseStudents.as_view()),
    path("cm_grades/", CMGrades.as_view()),
    path("students_grades/", StudentsGrades.as_view()),
]
