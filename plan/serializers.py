from rest_framework import serializers
from plan.models import RoughRequirement, DetailedRequirement
from plan.models import OfferingCourse, FieldOfStudy, IndicatorFactor
from plan.models import BasisTemplate

class SimpleOfferingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferingCourse
        fields = ['id', 'name']
        extra_kwargs = {'name': {'required': False}}

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

class SimpleOfferingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferingCourse
        fields = ["id", "name"]

class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = '__all__'

class IndicatorFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorFactor
        fields = '__all__'

class BasisTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasisTemplate
        fields = '__all__'

class ReadIndicatorFactorSerializer(serializers.ModelSerializer):
    offering_course = SimpleOfferingCourseSerializer()
    field_of_study = FieldOfStudySerializer()
    basis_templates = BasisTemplateSerializer(many=True)
    rough_requirement = serializers.IntegerField(source='detailed_requirement.rough_requirement.id')
    detailed_index = serializers.IntegerField(source='detailed_requirement.index')
    rough_index = serializers.IntegerField(source='detailed_requirement.rough_requirement.index')
    detailed_description = serializers.CharField(source='detailed_requirement.description')
    rough_description = serializers.CharField(source='detailed_requirement.rough_requirement.description')
    rough_title = serializers.CharField(source='detailed_requirement.rough_requirement.title')
    class Meta:
        model = IndicatorFactor
        fields = '__all__'