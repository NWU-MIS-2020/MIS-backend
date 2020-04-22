from django.urls import path
from user.views import AuthToken, TestEndpoint, Groups

urlpatterns = [
    path("login/", AuthToken.as_view()),
    path("test_endpoint/", TestEndpoint.as_view()),
    path("groups/", Groups.as_view()),
]
