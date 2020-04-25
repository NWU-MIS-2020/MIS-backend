from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from plan.models import OfferingCourse, BasisTemplate, IndicatorFactor
from user.models import Student, Teacher, CM


# Create your models here.

class Course(models.Model):
    ReviewStatusType = (
        ("未通过", "未通过"),
        ("未审核", "未审核"),
        ("已审核", "已审核"),
    )
    offering_course = models.ForeignKey(OfferingCourse, models.PROTECT, verbose_name="开设课程")
    start_date = models.DateField("开课日期", auto_now=False, auto_now_add=False)
    end_date = models.DateField("结课日期", auto_now=False, auto_now_add=False)
    short_description = models.CharField("简介", max_length=50, null=True, blank=True, default="")
    teachers = models.ManyToManyField(Teacher, "courses", verbose_name="负责教师")
    cms = models.ManyToManyField(CM, "courses", verbose_name="课程负责人")
    review_status = models.CharField("审核状态", choices=ReviewStatusType, default="未审核", max_length=10)
    review_comment = models.TextField("审核人评论", null=True, blank=True, default="")
    students = models.ManyToManyField(Student, "courses", verbose_name="学生", through='course.Grade')

    def __str__(self):
        return f"【{self.offering_course.name}】{self.short_description}, {self.start_date}-{self.end_date}"

    class Meta:
        verbose_name = verbose_name_plural = "历史课程"

class Grade(models.Model):
    course = models.ForeignKey(Course, models.PROTECT, "grades", verbose_name="课程")
    student = models.ForeignKey(Student, models.CASCADE, "grades", verbose_name="学生")
    final_marks = models.FloatField("结课分数", null=True, blank=True)

    def __str__(self):
        return f"{self.student} {self.course} : {self.final_marks}"

    class Meta:
        verbose_name = verbose_name_plural = "成绩和评价"
        unique_together = ["course", "student"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name='unique_grade'
            )
        ]

class Basis(models.Model):
    indicator_factor = models.ForeignKey(IndicatorFactor, models.PROTECT, verbose_name="支撑课程以及指标系数") # 只读
    course = models.ForeignKey(Course, models.CASCADE, "bases", verbose_name="历史课程")
    name = models.CharField("评价依据内容", max_length=50)
    full_marks = models.FloatField("满分值")

    def __str__(self):
        return f"{self.course}, {self.name}, {self.full_marks}"
    class Meta:
        verbose_name = verbose_name_plural = "历史评价依据"

@receiver(post_save, sender=Course, dispatch_uid="新建一个历史课程以后自动创建对应评价依据")
def create_bases_after_created_a_course(sender, instance, created, **kwargs):
    if not created:
        return
    for indicator_factor in instance.offering_course.indicator_factors.all():
        for basis_template in indicator_factor.basis_templates.all():
            Basis(
                course=instance,
                indicator_factor=basis_template.indicator_factor,
                name=basis_template.name,
                full_marks=basis_template.full_marks
            ).save()

class IndicatorMark(models.Model):
    indicator_factor = models.ForeignKey(IndicatorFactor, models.CASCADE, "indicator_marks", verbose_name="支撑课程以及指标系数")
    grade = models.ForeignKey(Grade, models.CASCADE, "indicator_marks", verbose_name="成绩和评价")
    total_marks = models.FloatField("加权平均评价分数", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.indicator_factor} {self.grade} : {self.total_marks}"

    class Meta:
        verbose_name = verbose_name_plural = "学生课程对应指标点评价值"
        unique_together = ["indicator_factor", "grade"]
        constraints = [
            models.UniqueConstraint(
                fields=["indicator_factor", "grade"],
                name='unique_indicator_mark'
            )
        ]

@receiver(post_save, sender=Grade, dispatch_uid="新建一个成绩与评价以后自动创建对应指标点评价")
def create_indicator_marks_after_created_a_grade(sender, instance, created, **kwargs):
    if not created:
        return
    for indicator_factor in instance.course.offering_course.indicator_factors.all():
        IndicatorMark(
            indicator_factor=indicator_factor,
            grade=instance,
        ).save()

class DetailedMark(models.Model):
    
    indicator_mark = models.ForeignKey(IndicatorMark, models.CASCADE, "detailed_marks", verbose_name="课程在指标点中总体评价", null=True)
    basis = models.ForeignKey(Basis, models.PROTECT, verbose_name="历史评级依据")
    marks = models.FloatField("实际分数", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.basis} {self.marks}"

    class Meta:
        verbose_name = verbose_name_plural = "学生课程对应指标点评价值细分"

@receiver(post_save, sender=IndicatorMark, dispatch_uid="新建一个课程对应指标点评价以后自动创建对应评价细分")
def create_detailed_marks_after_created_indicator_marks(sender, instance, created, **kwargs):
    if not created:
        return
    indicator_factor = instance.indicator_factor
    for basis in instance.grade.course.bases.filter(indicator_factor=indicator_factor):
        DetailedMark(
            indicator_mark=instance,
            basis=basis
        ).save()

@receiver(post_save, sender=DetailedMark, dispatch_uid="更新一个成绩评价以后自动计算总评价值")
def update_indicator_marks_after_updated_detailed_marks(sender, instance, created, **kwargs):
    if created:
        return
    indicator_mark = instance.indicator_mark
    a = b = 0.0
    for detailed_mark in indicator_mark.detailed_marks.all():
        if detailed_mark.marks is None:
            indicator_mark.total_marks = None
            indicator_mark.save()
            return
        a += detailed_mark.marks
        b += detailed_mark.basis.full_marks
    indicator_mark.total_marks = a/b # 要求历史课程必须有评价依据模版
    indicator_mark.save()
