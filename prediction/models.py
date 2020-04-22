from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from plan.models import RoughRequirement, DetailedRequirement
from course.models import Course, Grade
from user.models import Student, CM

class DetailedPrediction(models.Model):

    detailed_requirement = models.ForeignKey(DetailedRequirement, models.CASCADE, verbose_name="指标点", editable=False)
    student = models.ForeignKey(Student, models.CASCADE, verbose_name="学生", editable=False)
    indicator = models.FloatField("预测指标值", editable=False)

    def __str__(self):
        return "%s %s ? %f"%(self.student, self.detailed_requirement, self.indicator)

    class Meta:
        verbose_name = verbose_name_plural = "指标点达成度预测"
        unique_together = ["detailed_requirement", "student"]
        constraints = [
            models.UniqueConstraint(
                fields=["detailed_requirement", "student"],
                name='unique_detailed_prediction'
            )
        ]

# class Grade(models.Model):
#     course = models.ForeignKey(Course, models.PROTECT, verbose_name="课程")
#     student = models.ForeignKey(Student, models.CASCADE, verbose_name="学生")
#     final_marks = models.FloatField("结课分数", null=True, blank=True)
#     indicator = models.FloatField("评价分数", null=True, blank=True)
#     cm = models.ForeignKey(CM, models.PROTECT, verbose_name="审核人", null=True, blank=True)

#     def __str__(self):
#         return f"{self.student} {self.course} : {self.indicator}"

#     class Meta:
#         verbose_name = verbose_name_plural = "成绩和评价"
#         unique_together = ["course", "student"]
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["course", "student"],
#                 name='unique_grade'
#             )
#         ]

@receiver(post_save, sender=Student, dispatch_uid="新建一位学生以后")
def post_create_student(sender, instance, created, **kwargs):
    if not created:
        return
    for detailed_requirement in DetailedRequirement.objects.all():
        DetailedPrediction(
            student=instance,
            detailed_requirement=detailed_requirement,
            indicator=detailed_requirement.indicator_warning_line
        ).save()

@receiver(post_save, sender=Grade, dispatch_uid="修改成绩和评价以后")
def post_save_grade(sender, instance, **kwargs):
    if instance.indicator is None:
        return  # 如果没有添加评价值
    student = instance.student
    for indicator_factor_a in instance.course.offering_course.indicator_factors.all(): # 遍历这门课支撑的指标点关系
        detailed_requirement = indicator_factor_a.detailed_requirement # 获取指标点
        a = b = 0.0
        for indicator_factor_b in detailed_requirement.indicator_factors.all(): # 遍历指标点的所有支撑课程
            offering_course = indicator_factor_b.offering_course # 获取课程
            factor = indicator_factor_b.factor # 课程在指标点下的权重
            # 查最新的该课（考虑重修）
            grade = Grade.objects.filter(student=student, course__offering_course=offering_course).order_by('course__start_date').last()
            if grade is None:
                continue
            # print(grade, grade.indicator * factor, factor)
            a += grade.indicator * factor
            b += factor
        detailed_prediction = DetailedPrediction.objects.get(
            student=student, detailed_requirement=detailed_requirement
        )
        # print(detailed_requirement, a, b)
        detailed_prediction.indicator = a/b
        detailed_prediction.save()

class DetailedPredictionWarning(models.Model):
    detailed_prediction = models.OneToOneField(
        DetailedPrediction, models.CASCADE,
        verbose_name="指标点达成度预测", editable=False
    )

    def __str__(self):
        return "预警: %s"%(self.detailed_prediction)

    class Meta:
        verbose_name = verbose_name_plural = "指标点达成度预警"

@receiver(post_save, sender=DetailedPrediction, dispatch_uid="出现了新的指标点预测")
def post_update_detailed_prediction(sender, instance, created, **kwargs):
    if instance.indicator < instance.detailed_requirement.indicator_warning_line - 1e-6:
        DetailedPredictionWarning.objects.update_or_create(detailed_prediction=instance)
    else:
        try:
            DetailedPredictionWarning.objects.get(detailed_prediction=instance).delete()
        except ObjectDoesNotExist:
            pass
