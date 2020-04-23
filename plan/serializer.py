from rest_framework import serializers
from plan.models import RoughRequirement, DetailedRequirement, OfferingCourse

class RoughRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoughRequirement
        fields = ['id', 'index', 'title', 'description']

class DetailedRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailedRequirement
        fields = ['id', 'index', 'description', 'indicator_warning_line', 'rough_requirement']

class RequirementSerializer(serializers.ModelSerializer):
    detailed_requirements = DetailedRequirementSerializer(many=True)
    class Meta:
        model = RoughRequirement
        fields = ['id', 'index', 'title', 'description', 'detailed_requirements']

class OfferingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferingCourse
        fields = '__all__'