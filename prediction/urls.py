from django.urls import path
from prediction.views import DetailedPredictions, DetailedStudent

urlpatterns = [
    path("detailed_predictions/", DetailedPredictions.as_view()),
    path("student/", DetailedStudent.as_view()),
]
