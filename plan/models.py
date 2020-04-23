from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=50, verbose_name="专业方向名称")
    description = models.TextField("描述", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "专业方向"

class OfferingCourse(models.Model):
    ClassType = (
        ("通识通修课程", "通识通修课程"),
        ("专业平台课", "专业平台课"),
        ("专业核心课", "专业核心课"),
        ("集中实验环节", "集中实验环节"),
        ("专业分方向选修课", "专业分方向选修课"),
        ("专业选修课", "专业选修课"),
    )
    ClassProperty = (
        ('必修', '必修'),
        ('指选', '指选'),
        ('任选', '任选'),
        ('跨专业选修', '跨专业选修'),
    )
    course_type = models.CharField("课程类型", choices=ClassType, max_length=10)
    course_property = models.CharField("课程性质", choices=ClassProperty, max_length=10)
    number = models.CharField("课程编号", max_length=15, null=True, blank=True)
    name = models.CharField("课程名称", max_length=50)
    credit = models.FloatField("学分")
    total_period = models.IntegerField("总学时")
    teaching_period = models.IntegerField("课堂教学学时")
    experiment_period = models.IntegerField("课程实验学时", default=0)
    practice_period = models.IntegerField("课程实习学时", default=0)
    semester = models.CharField("开课学期", max_length=50, null=True, blank=True)
    description = models.TextField("描述", blank=True)

    def __str__(self):
        if self.number is None:
            return self.name
        return "%s[%s]"%(self.name, self.number)

    class Meta:
        verbose_name = verbose_name_plural = "开设课程"
        indexes = [
            models.Index(fields=['number']),
        ]


class RoughRequirement(models.Model):
    index = models.IntegerField("序号")
    title = models.CharField("标题", max_length=50)
    description = models.TextField("描述", blank=True)

    def __str__(self):
        return "%d: %s"%(self.id, self.title)

    class Meta:
        verbose_name = verbose_name_plural = "毕业要求"

class DetailedRequirement(models.Model):
    rough_requirement = models.ForeignKey(RoughRequirement, models.PROTECT, "detailed_requirements", verbose_name="毕业要求")
    index = models.IntegerField("子序号")
    description = models.TextField("描述", blank=True)
    indicator_warning_line = models.FloatField(default=0.65, verbose_name="预警指标值")

    def __str__(self):
        return "%d-%d"%(self.rough_requirement.index, self.index)

    class Meta:
        verbose_name = verbose_name_plural = "指标点"

class IndicatorFactor(models.Model):
    detailed_requirement = models.ForeignKey(DetailedRequirement, models.PROTECT, "indicator_factors",verbose_name="指标点")
    field_of_study = models.ForeignKey(FieldOfStudy, models.SET_NULL, null=True, blank=True, verbose_name="专业方向")
    offering_course = models.ForeignKey(OfferingCourse, models.PROTECT, "indicator_factors", verbose_name="课程")
    target = models.TextField("课程教学目标", null=True, blank=True, default="")
    # full_indicator = models.FloatField(default=1.0, verbose_name="指标系数")
    factor = models.FloatField("指标系数")


    def __str__(self):
        return "%s, %s, %s"%(self.detailed_requirement, self.field_of_study, self.offering_course)

    class Meta:
        verbose_name = verbose_name_plural = "支撑课程以及指标系数"
        unique_together = ["detailed_requirement", "field_of_study", "offering_course"]
        constraints = [
            models.UniqueConstraint(
                fields=["detailed_requirement", "field_of_study", "offering_course"],
                name='unique_indicator_factor'
            )
        ]

class BasisTemplate(models.Model):
    indicator_factor = models.ForeignKey(IndicatorFactor, models.CASCADE, "basis_templates", verbose_name="支撑课程以及指标系数")
    name = models.CharField("评价依据内容", max_length=50)
    full_marks = models.FloatField("满分值")
    def __str__(self):
        return f"{self.indicator_factor}, {self.name}, {self.full_marks}"
    class Meta:
        verbose_name = verbose_name_plural = "评价依据模版"
        constraints = [
            models.CheckConstraint(check=models.Q(full_marks__gte=0), name='full_marks_gte_0'),
        ]

@receiver(post_save, sender=IndicatorFactor, dispatch_uid="创建一个成绩评价以后增加几个评价模版")
def create_basis_templates_after_created_indicator_factor(sender, instance, created, **kwargs):
    if not created:
        return
    BasisTemplate(
        indicator_factor=instance,
        name="平时表现",
        full_marks=4
    ).save()
    BasisTemplate(
        indicator_factor=instance,
        name="作业",
        full_marks=6
    ).save()
    BasisTemplate(
        indicator_factor=instance,
        name="期末试题",
        full_marks=21
    ).save()
