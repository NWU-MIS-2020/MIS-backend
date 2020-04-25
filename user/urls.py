from django.urls import path
from user.views import AuthToken, TestEndpoint, Groups, Squads
from user.views import Students, Tutors, Teachers, PMs, CMs

urlpatterns = [
    path("login/", AuthToken.as_view()),
    path("test_endpoint/", TestEndpoint.as_view()),
    path("groups/", Groups.as_view()),
    path("squads/", Squads.as_view()),
    path("students/", Students.as_view()),
    path("tutors/", Tutors.as_view()),
    path("teachers/", Teachers.as_view()),
    path("cms/", CMs.as_view()),
    path("pms/", PMs.as_view()),
]
