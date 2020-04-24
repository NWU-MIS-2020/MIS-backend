from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from user.models import Student, Teacher, CM
from plan.models import OfferingCourse

from course.models import Course, Grade
from course.serializers import CourseSerializer, GradeSerializer, SimpleGradeSerializer

# Create your views here.

class Courses(APIView):
    """
    历史课程view
    """
    def get(self, request):
        """
        查询历史课程
        """
        data = {}
        id = request.GET.get('id', None)

        if id is not None:
            course = get_object_or_404(Course, id=id)
            serializer = CourseSerializer(course)
            return JsonResponse({"courses": [serializer.data]}, safe=False)

        student_username = request.GET.get('student_username', None)
        if student_username is not None:
            student = get_object_or_404(Student, user__username=student_username)
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return JsonResponse({"courses": serializer.data}, safe=False)

        teacher_username = request.GET.get('teacher_username', None)
        if teacher_username is not None:
            teacher = get_object_or_404(Teacher, user__username=teacher_username)
            courses = teacher.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return JsonResponse({"courses": serializer.data}, safe=False)
        
        cm_username = request.GET.get('cm_username', None)
        if cm_username is not None:
            cm = get_object_or_404(CM, user__username=cm_username)
            courses = cm.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return JsonResponse({"courses": serializer.data}, safe=False)

        offering_course_id = request.GET.get('offering_course_id', None)
        if offering_course_id is not None:
            courses = Course.objects.filter(offering_course=offering_course_id)
            serializer = CourseSerializer(courses, many=True)
            return JsonResponse({"courses": serializer.data}, safe=False)

        raise ParseError()

    def put(self, request):
        """
        修改历史课程
        """
        res = {"courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                course = get_object_or_404(Course, id=data["id"])
                if data.__contains__("offering_coures"):
                    data["offering_course"] = get_object_or_404(OfferingCourse, id=data["offering_course"])
                if data.__contains__("teachers"):
                    teachers = Teacher.objects.filter(user__username__in=[tea["username"] for tea in data.pop("teachers")])
                    course.teachers.set(teachers)
                if data.__contains__("cms"):
                    cms = CM.objects.filter(user__username__in=[cm["username"] for cm in data.pop("cms")])
                    course.cms.set(cms)
                course.__dict__.update(**data)
                course.save()
                serializer = CourseSerializer(course)
                res["courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加历史课程
        """
        res = {"courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                data["offering_course"] = get_object_or_404(OfferingCourse, id=data["offering_course"])
                teachers = Teacher.objects.filter(user__username__in=[tea["username"] for tea in data.pop("teachers")])
                cms = CM.objects.filter(user__username__in=[cm["username"] for cm in data.pop("cms")])
                course = Course.objects.create(**data)
                course.teachers.set(teachers)
                course.cms.set(cms)
                serializer = CourseSerializer(course)
                res["courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除历史课程
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                get_object_or_404(Course, id=data["id"]).delete()
        return Response()

class CourseStudents(APIView):
    """
    历史课程学生操作view
    """
    def post(self, request):
        res = {"course_students": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["course_students"]:
                course = get_object_or_404(Course, id=data["course"])
                student = get_object_or_404(Student, user__username=data["student"])
                grade = Grade.objects.create(course=course, student=student)
                serializer = SimpleGradeSerializer(grade)
                res["course_students"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)
        
    def delete(self, request):
        with transaction.atomic():
            for data in JSONParser().parse(request)["course_students"]:
                get_object_or_404(Grade, student__user__username=data["student"], course=data["course"]).delete()
        return Response()

class Grades(APIView):
    """
    成绩和评价view
    """
    def get(self, request):
        """
        查询成绩和评价
        """
        id = request.GET.get('id', None)
        if id is not None:
            grade = get_object_or_404(Grade, id=id)
            serializer = GradeSerializer(grade)
            return JsonResponse({"grades": [serializer.data]}, safe=False)

        student_username = request.GET.get('student_username', None)
        if student_username is not None:
            student = get_object_or_404(Student, user__username=student_username)
            grades = student.grades.all()
            serializer = GradeSerializer(grades, many=True)
            return JsonResponse({"grades": serializer.data}, safe=False)


        raise ParseError()

    def put(self, request):
        """
        修改历史课程
        """
        res = {"courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                course = get_object_or_404(Course, id=data["id"])
                if data.__contains__("offering_coures"):
                    data["offering_course"] = get_object_or_404(OfferingCourse, id=data["offering_course"])
                if data.__contains__("students"):
                    students = Student.objects.filter(user__username__in=[stu["username"] for stu in data.pop("students")])
                    course.students.set(students)
                if data.__contains__("teachers"):
                    teachers = Teacher.objects.filter(user__username__in=[tea["username"] for tea in data.pop("teachers")])
                    course.teachers.set(teachers)
                if data.__contains__("cms"):
                    cms = CM.objects.filter(user__username__in=[cm["username"] for cm in data.pop("cms")])
                    course.cms.set(cms)
                course.__dict__.update(**data)
                course.save()
                serializer = CourseSerializer(course)
                res["courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加历史课程
        """
        res = {"courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                data["offering_course"] = get_object_or_404(OfferingCourse, id=data["offering_course"])
                teachers = Teacher.objects.filter(user__username__in=[tea["username"] for tea in data.pop("teachers")])
                cms = CM.objects.filter(user__username__in=[cm["username"] for cm in data.pop("cms")])
                course = Course.objects.create(**data)
                for student in Student.objects.filter(user__username__in=[stu["username"] for stu in data.pop("students")]):
                    Grade.objects.create(course, student)
                course.teachers.set(teachers)
                course.cms.set(cms)
                serializer = CourseSerializer(course)
                res["courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除成绩和评价
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["courses"]:
                get_object_or_404(Course, id=data["id"]).delete()
        return Response()
