from django.contrib import admin

from .models import DetailedPrediction, DetailedPredictionWarning

# Register your models here.

# @admin.register(RoughPrediction)
# class RoughPredictionAdmin(admin.ModelAdmin):
#     pass

@admin.register(DetailedPrediction)
class DetailedPredictionAdmin(admin.ModelAdmin):
    list_display = ("student", "detailed_requirement", "indicator")

# @admin.register(Grade)
# class GradeAdmin(admin.ModelAdmin):
#     list_display = ("student", "course", "final_marks", "indicator")
#     list_filter = ("course", "student")

@admin.register(DetailedPredictionWarning)
class DetailedPredictionWaringAdmin(admin.ModelAdmin):
    list_display = ('student', "detailed_requirement", "indicator")

    def student(self, obj):
        return obj.detailed_prediction.student
    student.short_description = '学生'

    def detailed_requirement(self, obj):
        return obj.detailed_prediction.detailed_requirement
    detailed_requirement.short_description = "指标点"

    def indicator(self, obj):
        return obj.detailed_prediction.indicator
    indicator.short_description = "预测值"
