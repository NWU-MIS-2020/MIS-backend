from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.models import Student, Teacher, CM
from user.serializers import SimpleStudentSerializer, SimpleTeacherSerializer, SimpleCMSerializer

from plan.models import OfferingCourse
from plan.serializers import SimpleOfferingCourseSerializer


from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    offering_course = SimpleOfferingCourseSerializer()
    teachers = SimpleTeacherSerializer(many=True)
    cms = SimpleCMSerializer(many=True)
    students = SimpleStudentSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

