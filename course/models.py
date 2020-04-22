from django.db import models
from plan.models import OfferingCourse
from user.models import Student, Teacher, CM


# Create your models here.

class Course(models.Model):
    offering_course = models.ForeignKey(OfferingCourse, models.PROTECT, verbose_name="开设课程")
    start_date = models.DateField("开课日期", auto_now=False, auto_now_add=False)
    end_date = models.DateField("结课日期", auto_now=False, auto_now_add=False)
    short_description = models.CharField("简介", max_length=50, null=True, blank=True)
    teachers = models.ManyToManyField(Teacher, verbose_name="负责教师")
    cms = models.ManyToManyField(CM, verbose_name="课程负责人")

    def __str__(self):
        return f"【{self.offering_course.name}】{self.short_description}, {self.start_date}-{self.end_date}"

    class Meta:
        verbose_name = verbose_name_plural = "历史课程"

class Grade(models.Model):
    course = models.ForeignKey(Course, models.PROTECT, verbose_name="课程")
    student = models.ForeignKey(Student, models.CASCADE, verbose_name="学生")
    final_marks = models.FloatField("结课分数", null=True, blank=True)
    indicator = models.FloatField("评价分数", null=True, blank=True)
    cm = models.ForeignKey(CM, models.PROTECT, verbose_name="审核人", null=True, blank=True)

    def __str__(self):
        return f"{self.student} {self.course} : {self.indicator}"

    class Meta:
        verbose_name = verbose_name_plural = "成绩和评价"
        unique_together = ["course", "student"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name='unique_grade'
            )
        ]