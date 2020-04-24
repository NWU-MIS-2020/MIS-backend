from django.contrib.auth.models import Group
from rest_framework import serializers

from user.models import Student, Teacher, Tutor, CM, PM

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name',]

class SimpleStudentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', required=False)

    class Meta:
        model = Student
        fields = ['username', 'name']

class SimpleTeacherSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', required=False)

    class Meta:
        model = Teacher
        fields = ['username', 'name']

class SimpleTutorSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', required=False)

    class Meta:
        model = Tutor
        fields = ['username', 'name']

class SimpleCMSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', required=False)

    class Meta:
        model = CM
        fields = ['username', 'name']

class SimplePMSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', required=False)

    class Meta:
        model = PM
        fields = ['username', 'name']
