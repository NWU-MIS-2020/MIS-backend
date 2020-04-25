from django.contrib.auth.models import Group, User
from rest_framework import serializers

from user.models import Student, Teacher, Tutor, CM, PM, Squad

class CreateUserSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['username', 'name']

    def create(self, validated_data):
        password = validated_data['username']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name',]

class UpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        read_only_fields = ["username"]
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        return instance

class TutorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Tutor
        exclude = ['user']

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Student
        exclude = ['user']

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


class SquadSerializer(serializers.ModelSerializer):
    students_info = SimpleStudentSerializer(source='students', many=True, read_only=True)
    tutor_info = SimpleTutorSerializer(source='tutor', read_only=True)
    class Meta:
        model = Squad
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Teacher
        exclude = ['user']

class CMSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = CM
        exclude = ['user']

class PMSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = PM
        exclude = ['user']
