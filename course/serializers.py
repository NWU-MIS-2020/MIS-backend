from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.models import Student, Teacher, CM
from user.serializers import SimpleStudentSerializer, SimpleTeacherSerializer, SimpleCMSerializer

from plan.models import OfferingCourse
from plan.serializers import SimpleOfferingCourseSerializer


from course.models import Course, Grade, Basis, IndicatorMark, DetailedMark

class BasisMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basis
        fields = ["id", "name", "full_marks"]
        read_only_fields = ["id", "name", "full_marks"]

class CourseSerializer(serializers.ModelSerializer):
    offering_course = SimpleOfferingCourseSerializer()
    teachers = SimpleTeacherSerializer(many=True)
    cms = SimpleCMSerializer(many=True)
    students = SimpleStudentSerializer(many=True)
    bases = BasisMarkSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class SimpleCourseSerializer(serializers.ModelSerializer):
    offering_course = SimpleOfferingCourseSerializer()
    class Meta:
        model = Course
        fields = ["id", "offering_course"]
        read_only_fields = ["id", "offering_course"]

class DetailedMarkSerializer(serializers.ModelSerializer):
    basis = BasisMarkSerializer(read_only=True)
    class Meta:
        model = DetailedMark
        fields = ["id", "basis", "marks"]
        read_only_fields = ["id", "basis"]

class IndicatorMarkSerializer(serializers.ModelSerializer):
    detailed_marks = DetailedMarkSerializer(many=True)
    class Meta:
        model = IndicatorMark
        fields = ["id", "indicator_factor", "total_marks", "detailed_marks"]
        read_only_fields = ["id", "indicator_factor"]

class GradeSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer(read_only=True)
    student = SimpleStudentSerializer(read_only=True)
    indicator_marks = IndicatorMarkSerializer(many=True)
    class Meta:
        model = Grade
        fields = '__all__'

class SimpleGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "course", "student", "final_marks"]
        read_only_fields = ["id"]
