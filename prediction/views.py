from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import Student, Squad
from plan.models import RoughRequirement
from course.models import IndicatorMark

from prediction.models import DetailedPrediction, DetailedPredictionWarning



# Create your views here.

def get_predictions_by_student(student):
    student_info = {
        "username": student.user.username,
        "name": student.user.first_name,
        "rough_predictions" : [],
        "total_indicator" : None
    }
    for rough_requirement in RoughRequirement.objects.all():
        rough_prediction_info = {
            "indicator": None,
            "rough_requirement_id": rough_requirement.id,
            "rough_requirement_index": rough_requirement.index,
            "is_lt_wil": False,
            "detailed_predictions": []
        }
        for detailed_prediction in student.detailed_predictions.filter(detailed_requirement__rough_requirement=rough_requirement).all():
            detailed_prediction_info = {
                "indicator": detailed_prediction.indicator,
                "detailed_requirement_id": detailed_prediction.detailed_requirement.id,
                "detailed_requirement_index": detailed_prediction.detailed_requirement.index,
                "is_lt_wil": False
            }
            if detailed_prediction.indicator is not None:
                if rough_prediction_info["indicator"] is None:
                    rough_prediction_info["indicator"] = detailed_prediction.indicator
                    student_info["total_indicator"] = rough_prediction_info["indicator"]
                else:
                    rough_prediction_info["indicator"] = min(detailed_prediction.indicator, rough_prediction_info["indicator"])
                    student_info["total_indicator"] = min(student_info["total_indicator"], rough_prediction_info["indicator"])
            if DetailedPredictionWarning.objects.filter(detailed_prediction=detailed_prediction.id).exists():
                detailed_prediction_info["is_lt_wil"] = True
                rough_prediction_info["is_lt_wil"] = True
            rough_prediction_info["detailed_predictions"].append(detailed_prediction_info)
        student_info["rough_predictions"].append(rough_prediction_info)
        
    return student_info

class DetailedPredictions(APIView):
    """
    毕业要求和对应指标点预测view
    """
    def get(self, request):
        """
        查询预测
        """
        student_username = request.GET.get("student_username", None)
        if student_username is not None:
            student = get_object_or_404(Student, user__username=student_username)
            data = get_predictions_by_student(student)
            return JsonResponse({"students":[data]}, safe=False)
        squad_id = request.GET.get("squad_id", None)
        if squad_id is not None:
            res = {
                "students": []
            }
            squad = get_object_or_404(Squad, id=squad_id)
            for student in squad.students.all():
                data = get_predictions_by_student(student)
                res["students"].append(data)
            return JsonResponse(res, safe=False)
        raise ParseError()

class DetailedStudent(APIView):
    """
    单个学生详细指标点
    """
    def get(self, request):
        res = {}
        student = get_object_or_404(Student, user__username = request.GET.get("student_username"))
        student_field_of_study = student.field_of_study
        student_courses = student.grades.values("course").all()
        student_grades = student.grades.all()
        res["name"] = student.user.first_name
        res["total_indicator"] = None
        if student_field_of_study is not None:
            res["field_of_study_name"] = student_field_of_study.name
        else:
            res["field_of_study_name"] = None
        res["rough_requirements"] = []
        for rough_requirement in RoughRequirement.objects.all():
            # 毕业要求
            rough_requirement_info = {
                "indicator": None, #!!!!
                "index": rough_requirement.index,
                "description": rough_requirement.description,
                "title": rough_requirement.title,
                "is_lt_wil": False,
                "detailed_requirements": []
            }
            for detailed_requirement in rough_requirement.detailed_requirements.all():
                # 指标点
                detailed_requirement_info = {
                    "indicator": None,
                    "index": detailed_requirement.index,
                    "description": detailed_requirement.description,
                    "is_lt_wil": False,
                    "courses": []
                }
                if DetailedPredictionWarning.objects.filter(detailed_prediction__detailed_requirement=detailed_requirement.id).exists():
                    detailed_requirement_info["is_lt_wil"] = True
                    rough_requirement_info["is_lt_wil"] = True
                for indicator_factor in detailed_requirement.indicator_factors.all(): #.filter(field_of_study__in=[None, student_field_of_study]):
                    if indicator_factor.field_of_study is not None:
                        if student_field_of_study is not None and not indicator_factor.id == student_field_of_study.id:
                            break
                    # 支撑课程及指标系数
                    
                    offering_course = indicator_factor.offering_course # 开设课程
                    cur_student_grades = student_grades.filter(course__offering_course=offering_course)
                    if cur_student_grades.exists():
                        cur_student_grade = cur_student_grades.order_by('course__start_date').last() # 找到历史课程成绩
                        indicator_mark = get_object_or_404(IndicatorMark, grade=cur_student_grade, indicator_factor=indicator_factor)
                        course_info = {
                            "factor": indicator_factor.factor,
                            "indicator": indicator_mark.total_marks,
                            "name": offering_course.name
                        }
                        detailed_requirement_info["courses"].append(course_info)
                sum_indicator = 0
                for course_info in detailed_requirement_info["courses"]:
                    indicator = course_info["indicator"]
                    if indicator is None:
                        detailed_requirement_info["indicator"] = None
                        break
                    sum_indicator += indicator * course_info["factor"]
                else:
                    if not len(detailed_requirement_info["courses"]) == 0:
                        detailed_requirement_info["indicator"] = sum_indicator

                rough_requirement_info["detailed_requirements"].append(detailed_requirement_info)
            
            for detailed_requirement_info in rough_requirement_info["detailed_requirements"]:
                indicator = detailed_requirement_info["indicator"]
                if indicator is None:
                    rough_requirement_info["indicator"] = None
                    break
                if rough_requirement_info["indicator"] is None:
                    rough_requirement_info["indicator"] = indicator
                else:
                    rough_requirement_info["indicator"] = min(indicator, rough_requirement_info["indicator"])

            res["rough_requirements"].append(rough_requirement_info)

        for rough_requirement_info in res["rough_requirements"]:
            indicator = rough_requirement_info["indicator"]
            if indicator is None:
                res["total_indicator"] = None
                break
            if res["total_indicator"] is None:
                res["total_indicator"] = indicator
            else:
                res["total_indicator"] = min(indicator, res["total_indicator"])

        return JsonResponse(res, safe=False)
