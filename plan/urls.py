from django.urls import path
from plan.views import Requirements, RoughRequirements, DetailedRequirements
from plan.views import OfferingCourses, FieldsOfStudy, IndicatorFactors
from plan.views import BasisTemplates

urlpatterns = [
    path("requirements/", Requirements.as_view()),
    path("rough_requirements/", RoughRequirements.as_view()),
    path("detailed_requirements/", DetailedRequirements.as_view()),
    path("offering_courses/", OfferingCourses.as_view()),
    path("fields_of_study/", FieldsOfStudy.as_view()),
    path("indicator_factors/", IndicatorFactors.as_view()),
    path("basis_templates/", BasisTemplates.as_view()),
]
