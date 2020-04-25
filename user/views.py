from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import GroupSerializer, UpdatePasswordSerializer, CreateUserSerializer
from user.serializers import SquadSerializer, StudentSerializer, TutorSerializer
from user.serializers import TeacherSerializer, CMSerializer, PMSerializer
from user.models import Squad, Student, Tutor, Teacher, CM, PM

# Create your views here.

class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        账号密码登入
        """
        response = super().post(request, *args, **kwargs)
        response.data['token'] = 'Token '+response.data['token']
        response.set_cookie('token', response.data['token'])
        return response

class Groups(APIView):
    """
    组
    """
    def get(self, request):
        """
        获取组
        """
        user = request.user
        serializer = GroupSerializer(user.groups.all(), many=True)
        res = {
            "groups": serializer.data,
            "name": user.first_name,
            "username": user.username,
        }
        return JsonResponse(res, safe=False)

class UpdatePassword(APIView):
    """
    修改密码
    """
    def put(self, request):
        """
        修改密码
        """
        res = {"users": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["users"]:
                user = get_object_or_404(User, username=data["username"])
                serializer = UpdatePasswordSerializer(user, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError()
                serializer.save()
                res["users"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

def create_user_by_data(data):
    name = data.pop("name", None)
    username = data.pop("username", None)
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        user = User.objects.create(username=username)
        user.set_password(username)
        if name:
            user.first_name = name
        user.save()
    return user

class Tutors(APIView):
    """
    导员view
    """
    def get(self, request):
        """
        查询导员
        """
        username = request.GET.get("username", None)
        if username is not None:
            tutor = get_object_or_404(Tutor, user__username=username)
            serializer = TutorSerializer(tutor)
            return JsonResponse({"tutors": [serializer.data]}, safe=False)
        else:
            tutors = Tutor.objects.all()
            serializer = TutorSerializer(tutors, many=True)
            return JsonResponse({"tutors": serializer.data}, safe=False)

    def post(self, request):
        """
        增加导员
        """
        res = {"tutors": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["tutors"]:
                user = create_user_by_data(data)
                tutor = Tutor.objects.create(user=user, **data)
                serializer = TutorSerializer(tutor)
                res["tutors"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除导员
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["tutors"]:
                Tutor.objects.get(user__username=data["username"]).delete()
        return Response()

class Squads(APIView):
    """
    班级view
    """
    def get(self, request):
        """
        查询班级
        """
        squads = Squad.objects.all()
        serializer = SquadSerializer(squads, many=True)
        return JsonResponse({"squads": serializer.data}, safe=False)

    def put(self, request):
        """
        修改班级
        """
        res = {"squads": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["squads"]:
                squad = get_object_or_404(Squad, id=data["id"])
                serializer = SquadSerializer(squad, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["squads"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加班级
        """
        res = {"squads": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["squads"]:
                serializer = SquadSerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["squads"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除班级
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["squads"]:
                Squad.objects.get(id=data["id"]).delete()
        return Response()



class Students(APIView):
    """
    学生view
    """
    def get(self, request):
        """
        查询学生
        """
        username = request.GET.get("username", None)
        if username is not None:
            student = get_object_or_404(Student, user__username=username)
            serializer = StudentSerializer(student)
            return JsonResponse({"students": [serializer.data]}, safe=False)
        squad_id = request.GET.get("squad_id", None)
        if squad_id is not None:
            students = Student.objects.filter(squad=squad_id)
            serializer = StudentSerializer(students, many=True)
            return JsonResponse({"students": serializer.data}, safe=False)

    def put(self, request):
        """
        修改学生
        """
        res = {"students": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["students"]:
                student = get_object_or_404(Student, user__username=data["username"])
                serializer = StudentSerializer(student, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["students"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加学生
        """
        res = {"students": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["students"]:
                user = create_user_by_data(data)
                if data.__contains__("squad"):
                    data["squad"] = get_object_or_404(Squad, id=data["squad"])
                student = Student.objects.create(user=user, **data)
                serializer = StudentSerializer(student)
                res["students"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除学生
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["students"]:
                Student.objects.get(user__username=data["username"]).delete()
        return Response()


class Teachers(APIView):
    """
    教师view
    """
    def get(self, request):
        """
        查询教师
        """
        username = request.GET.get("username", None)
        if username is not None:
            teacher = get_object_or_404(Teacher, user__username=username)
            serializer = TeacherSerializer(teacher)
            return JsonResponse({"teachers": [serializer.data]}, safe=False)
        else:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return JsonResponse({"teachers": serializer.data}, safe=False)

    def post(self, request):
        """
        增加教师
        """
        res = {"teachers": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["teachers"]:
                user = create_user_by_data(data)
                teacher = Teacher.objects.create(user=user, **data)
                serializer = TeacherSerializer(teacher)
                res["teachers"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除教师
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["teachers"]:
                Teacher.objects.get(user__username=data["username"]).delete()
        return Response()


class CMs(APIView):
    """
    课程负责人view
    """
    def get(self, request):
        """
        查询课程负责人
        """
        username = request.GET.get("username", None)
        if username is not None:
            cm = get_object_or_404(CM, user__username=username)
            serializer = CMSerializer(cm)
            return JsonResponse({"cms": [serializer.data]}, safe=False)
        else:
            cms = CM.objects.all()
            serializer = CMSerializer(cms, many=True)
            return JsonResponse({"cms": serializer.data}, safe=False)

    def post(self, request):
        """
        增加课程负责人
        """
        res = {"cms": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["cms"]:
                user = create_user_by_data(data)
                cm = CM.objects.create(user=user, **data)
                serializer = CMSerializer(cm)
                res["cms"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除课程负责人
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["cms"]:
                CM.objects.get(user__username=data["username"]).delete()
        return Response()


class PMs(APIView):
    """
    专业负责人view
    """
    def get(self, request):
        """
        查询专业负责人
        """
        username = request.GET.get("username", None)
        if username is not None:
            pm = get_object_or_404(PM, user__username=username)
            serializer = CMSerializer(pm)
            return JsonResponse({"pms": [serializer.data]}, safe=False)
        else:
            pms = PM.objects.all()
            serializer = PMSerializer(pms, many=True)
            return JsonResponse({"pms": serializer.data}, safe=False)

    def post(self, request):
        """
        增加专业负责人
        """
        res = {"pms": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["pms"]:
                user = create_user_by_data(data)
                pm = PM.objects.create(user=user, **data)
                serializer = PMSerializer(pm)
                res["pms"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除导员
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["pms"]:
                PM.objects.get(user__username=data["username"]).delete()
        return Response()

class TestEndpoint(APIView):
    """
    测试Endpoint
    """
    def get(self, request):
        return Response("Good Job! It is a GET method.")
    
    def post(self, request):
        return Response("Good Job! It is a POST method.")
        template = [
            {
                "id":"1",
                "names": [
                    "韩文清",
                    "张新杰",
                    "张佳乐",
                    "林敬言",
                    "宋奇英",
                    "秦牧云",
                    "白言飞",
                    "郑乘风",
                    "于天",
                    "李艺博",
                    "季冷",
                    "贾世明",
                    "王驰轩",
                ]
            },
            {
                "id":"2",
                "names": [
                    "孙翔",
                    "吴雪峰",
                    "刘皓",
                    "贺铭",
                    "张家兴",
                    "肖时钦",
                    "申建",
                    "王泽",
                    "郭阳",
                    "方锋然",
                    "孟永鸣",
                    "李睿",
                    "白胜先",
                    "邱非",
                    "闻理",
                    "夏仲天",
                    "陈夜辉",
                ]
            },
            {
                "id":"3",
                "names": [
                    "王杰希",
                    "许斌",
                    "高英杰",
                    "刘小别",
                    "袁柏清",
                    "梁方",
                    "柳非",
                    "周烨柏",
                    "肖云",
                    "李济",
                    "林杰",
                    "方士谦",
                    "邓复升",
                ]
            },
            {
                "id":"4",
                "names": [
                    "叶修",
                    "苏沐橙",
                    "方锐",
                    "唐柔",
                    "包荣兴",
                    "乔一帆",
                    "罗辑",
                    "莫凡",
                    "安文逸",
                    "魏琛",
                    "陈果",
                    "伍晨",
                    "关榕飞",
                ]
            }
        ]
        res = {"students": []}
        with transaction.atomic():
            username = 2017666000
            for squad in template:
                squad_id = squad["id"]
                for name in squad["names"]:
                    username += 1
                    data = {
                        "username": str(username),
                        "name": name,
                        "squad": squad_id,
                        "admission_date": "2017-9-1",
                        "graduation_date": "2021-7-1"
                    }
                    user = create_user_by_data(data)
                    if data.__contains__("squad"):
                        data["squad"] = get_object_or_404(Squad, id=data["squad"])
                    student = Student.objects.create(user=user, **data)
                    serializer = StudentSerializer(student)
                    res["students"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)
        
    
    def put(self, request):
        return Response("Good Job! It is a PUT method.")
    
    def delete(self, request):
        return Response("Good Job! It is a DELETE method.")