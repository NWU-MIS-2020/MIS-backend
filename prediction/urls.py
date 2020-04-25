from django.urls import path
from prediction.views import DetailedPredictions

urlpatterns = [
    path("detailed_predictions/", DetailedPredictions.as_view()),
]
