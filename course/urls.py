from django.urls import path
from course.views import Courses

urlpatterns = [
    path("courses/", Courses.as_view()),
]
