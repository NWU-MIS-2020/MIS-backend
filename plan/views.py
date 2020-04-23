from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from plan.models import RoughRequirement, DetailedRequirement
from plan.models import OfferingCourse, FieldOfStudy, IndicatorFactor
from plan.serializer import RoughRequirementSerializer, DetailedRequirementSerializer, RequirementSerializer
from plan.serializer import OfferingCourseSerializer, FieldOfStudySerializer, IndicatorFactorSerializer

# Create your views here.

class Requirements(APIView):
    """
    毕业要求和对应指标点view
    """
    def get(self, request):
        """
        查询毕业要求和对应指标点
        """
        serializer = RequirementSerializer(RoughRequirement.objects.all(), many=True)
        return JsonResponse({"rough_requirements": serializer.data}, safe=False)

class RoughRequirements(APIView):
    """
    毕业要求view
    """
    def get(self, request):
        """
        查询毕业要求
        """
        serializer = RoughRequirementSerializer(RoughRequirement.objects.all(), many=True)
        return JsonResponse({"rough_requirements": serializer.data}, safe=False)

    def put(self, request):
        """
        修改毕业要求
        """
        res = {"rough_requirements": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["rough_requirements"]:
                rough_requirement = get_object_or_404(RoughRequirement, id=data["id"])
                serializer = RoughRequirementSerializer(rough_requirement, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError()
                serializer.save()
                res["rough_requirements"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加毕业要求
        """
        res = {"rough_requirements": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["rough_requirements"]:
                if data.get("id", None) is not None:
                    raise ParseError()  # 增加不能有主键
                serializer = RoughRequirementSerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError()
                serializer.save()
                res["rough_requirements"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除毕业要求
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["rough_requirements"]:
                RoughRequirement.objects.get(id=data["id"]).delete()
        return Response()


class DetailedRequirements(APIView):
    """
    指标点view
    """
    def get(self, request):
        """
        查询指标点
        """
        data = JSONParser().parse(request)["detailed_requirements"]
        detailed_requirements = DetailedRequirement.objects.filter(id__in=[d["id"] for d in data])
        serializer = DetailedRequirementSerializer(detailed_requirements, many=True)
        return JsonResponse({"detailed_requirements": serializer.data}, safe=False)

    def put(self, request):
        """
        修改指标点
        """
        res = {"detailed_requirements": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["detailed_requirements"]:
                detailed_requirement = get_object_or_404(DetailedRequirement, id=data["id"])
                serializer = DetailedRequirementSerializer(detailed_requirement, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["detailed_requirements"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加指标点
        """
        res = {"detailed_requirements": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["detailed_requirements"]:
                print(data)
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                serializer = DetailedRequirementSerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["detailed_requirements"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除毕业要求
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["detailed_requirements"]:
                DetailedRequirement.objects.get(id=data["id"]).delete()
        return Response()

class OfferingCourses(APIView):
    """
    开设课程view
    """
    def get(self, request):
        """
        查询开设课程
        """
        # data = JSONParser().parse(request)
        id = request.GET.get("id", None)
        if id is None:
            offering_courses = OfferingCourse.objects.all()
            serializer = OfferingCourseSerializer(offering_courses, many=True)
            return JsonResponse({"offering_courses": serializer.data}, safe=False)
        else:
            offering_course = get_object_or_404(OfferingCourse, id=id)
            serializer = OfferingCourseSerializer(offering_course)
            return JsonResponse({"offering_courses": [serializer.data]}, safe=False)

    def put(self, request):
        """
        修改开设课程
        """
        res = {"offering_courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["offering_courses"]:
                offering_course = get_object_or_404(OfferingCourse, id=data["id"])
                serializer = OfferingCourseSerializer(offering_course, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["offering_courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加开设课程
        """
        res = {"offering_courses": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["offering_courses"]:
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                serializer = OfferingCourseSerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["offering_courses"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除开设课程
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["offering_courses"]:
                get_object_or_404(OfferingCourse, id=data["id"]).delete()
        return Response()


class FieldsOfStudy(APIView):
    """
    专业方向view
    """
    def get(self, request):
        """
        查询专业方向
        """
        id = request.GET.get("id", None)
        if id is None:
            fields_of_study = FieldOfStudy.objects.all()
            serializer = FieldOfStudySerializer(fields_of_study, many=True)
            return JsonResponse({"fields_of_study": serializer.data}, safe=False)
        else:
            field_of_study = get_object_or_404(FieldOfStudy, id=id)
            serializer = FieldOfStudySerializer(field_of_study)
            return JsonResponse({"fields_of_study": [serializer.data]}, safe=False)

    def put(self, request):
        """
        修改专业方向
        """
        res = {"fields_of_study": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["fields_of_study"]:
                field_of_study = get_object_or_404(FieldOfStudy, id=data["id"])
                serializer = FieldOfStudySerializer(field_of_study, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["fields_of_study"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加专业方向
        """
        res = {"fields_of_study": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["fields_of_study"]:
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                serializer = FieldOfStudySerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["fields_of_study"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除专业方向
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["fields_of_study"]:
                get_object_or_404(FieldOfStudy, id=data["id"]).delete()
        return Response()

class IndicatorFactors(APIView):
    """
    支撑课程view
    """
    def get(self, request):
        """
        查询支撑课程
        """
        data = {}
        id = request.GET.get('id', None)
        detailed_requirement_id = request.GET.get('detailed_requirement_id', None)
        offering_course_id = request.GET.get('offering_course_id', None)
        field_of_study_id = request.GET.get('field_of_study_id', None)
        if id is not None:
            data["id"] = id
        if detailed_requirement_id is not None:
            data["detailed_requirement"] = detailed_requirement_id
        if offering_course_id is not None:
            data["offering_course"] = offering_course_id
        if field_of_study_id is not None:
            data["field_of_study"] = field_of_study_id
        # if data is None:
        #     raise ParseError("禁止查询全部")
        indicator_factors = IndicatorFactor.objects.filter(**data)
        serializer = IndicatorFactorSerializer(indicator_factors, many=True)
        return JsonResponse({"indicator_factors": serializer.data}, safe=False)

    def put(self, request):
        """
        修改支撑课程
        """
        res = {"indicator_factors": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["indicator_factors"]:
                indicator_factor = get_object_or_404(IndicatorFactor, id=data["id"])
                serializer = IndicatorFactorSerializer(indicator_factor, data=data, partial=True)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["indicator_factors"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def post(self, request):
        """
        增加支撑课程
        """
        res = {"indicator_factors": []}
        with transaction.atomic():
            for data in JSONParser().parse(request)["indicator_factors"]:
                if data.get("id", None) is not None:
                    raise ParseError("不能有主键")  # 增加不能有主键
                serializer = IndicatorFactorSerializer(data=data)
                if not serializer.is_valid():
                    raise ParseError(serializer.errors)
                serializer.save()
                res["indicator_factors"].append(serializer.data)
        return JsonResponse(res, status=200, safe=False)

    def delete(self, request):
        """
        删除专业方向
        """
        with transaction.atomic():
            for data in JSONParser().parse(request)["indicator_factors"]:
                get_object_or_404(IndicatorFactor, id=data["id"]).delete()
        return Response()
