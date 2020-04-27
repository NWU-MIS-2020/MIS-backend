from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from plan.models import RoughRequirement, DetailedRequirement
from course.models import Course, IndicatorMark
from user.models import Student, CM

class DetailedPrediction(models.Model):

    detailed_requirement = models.ForeignKey(DetailedRequirement, models.CASCADE, verbose_name="指标点", editable=False)
    student = models.ForeignKey(Student, models.CASCADE, "detailed_predictions", verbose_name="学生", editable=False)
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

@receiver(post_save, sender=IndicatorMark, dispatch_uid="修改评价以后")
def post_save_grade(sender, instance, **kwargs):
    if instance.total_marks is None:
        return  # 没有添加评价值 待解决：评价值可能会从有到无
    a = 0.0 # 分子
    cst = 0 # 分母
    student = instance.grade.student
    detailed_requirement = instance.indicator_factor.detailed_requirement
    for indicator_factor in detailed_requirement.indicator_factors.all():
        indicator_mark = IndicatorMark.objects.filter(
            grade__student=student, indicator_factor=indicator_factor
            ).order_by('grade__course__start_date').last()
        if indicator_mark is None or indicator_mark.total_marks is None:
            continue
        a += indicator_mark.total_marks * indicator_factor.factor
        cst += 1
    if cst == 0:
        return
    detailed_prediction, b = DetailedPrediction.objects.get_or_create(
        student=student, detailed_requirement=detailed_requirement
    )
    detailed_prediction.indicator = a/cst # 加权平均
    detailed_prediction.save()

class DetailedPredictionWarning(models.Model):
    detailed_prediction = models.OneToOneField(
        DetailedPrediction, models.CASCADE, related_name ='detailed_prediction_warning',
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
