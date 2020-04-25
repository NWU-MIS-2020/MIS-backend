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

from prediction.models import DetailedPrediction, DetailedPredictionWarning



# Create your views here.

def get_predictions_by_student(student):
    student_info = {
        "username": student.user.username,
        "name": student.user.first_name,
        "rough_predictions_info" : []
    }
    for rough_requirement in RoughRequirement.objects.all():
        rough_prediction_info = {
            "indicator": None,
            "rough_requirement_id": rough_requirement.id,
            "rough_requirement_index": rough_requirement.index,
            "is_lt_wil": False,
            "detailed_predictions": []
        }
        for detailed_prediction in student.detailed_predictions.all():
            detailed_prediction_info = {
                "indicator": detailed_prediction.indicator,
                "detailed_requirement_id": detailed_prediction.detailed_requirement.id,
                "detailed_requirement_index": detailed_prediction.detailed_requirement.index,
                "is_lt_wil": False
            }
            if detailed_prediction.indicator is not None:
                if rough_prediction_info["indicator"] is None:
                    rough_prediction_info["indicator"] = detailed_prediction.indicator
                else:
                    rough_prediction_info["indicator"] = min(detailed_prediction.indicator, rough_prediction_info["indicator"])
            if DetailedPredictionWarning.objects.filter(detailed_prediction=detailed_prediction.id).exists():
                detailed_prediction_info["is_lt_wil"] = True
                rough_prediction_info["is_lt_wil"] = True
            rough_prediction_info["detailed_predictions"].append(detailed_prediction_info)
        student_info["rough_predictions_info"].append(rough_prediction_info)
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
            return JsonResponse({"students":[data]}, safe=False)
        raise ParseError()
