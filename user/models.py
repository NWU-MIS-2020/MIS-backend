from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

from plan.models import FieldOfStudy

from rest_framework.authtoken.models import Token

# Create your models here.

@receiver(post_save, sender=User, dispatch_uid="创建之后要自动生成令牌")
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Teacher(models.Model):
    user = models.OneToOneField(User, models.CASCADE, "username", verbose_name="账户", primary_key=True)

    def __str__(self):
        return "%s(%s)"%(self.user.first_name, self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "教师"

@receiver(post_save, sender=Teacher, dispatch_uid="创建之后要自动添加至教师组")
def add_teacher_group(sender, instance=None, created=False, **kwargs):
    if created:
        group, b = Group.objects.get_or_create(name="教师")
        instance.user.groups.add(group)

class Tutor(models.Model):
    user = models.OneToOneField(User, models.CASCADE, "username", verbose_name="账户", primary_key=True)

    def __str__(self):
        return "%s(%s)"%(self.user.first_name, self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "导员"

@receiver(post_save, sender=Tutor, dispatch_uid="创建之后要自动添加至导员组")
def add_tutor_group(sender, instance=None, created=False, **kwargs):
    if created:
        group, b = Group.objects.get_or_create(name="导员")
        instance.user.groups.add(group)

class CM(models.Model):
    user = models.OneToOneField(User, models.CASCADE, "username", verbose_name="账户", primary_key=True)

    def __str__(self):
        return "%s(%s)"%(self.user.first_name, self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "课程负责人"

@receiver(post_save, sender=CM, dispatch_uid="创建之后要自动添加至课程负责人组")
def add_cm_group(sender, instance=None, created=False, **kwargs):
    if created:
        group, b = Group.objects.get_or_create(name="课程负责人")
        instance.user.groups.add(group)

class PM(models.Model):
    user = models.OneToOneField(User, models.CASCADE, "username", verbose_name="账户", primary_key=True)

    def __str__(self):
        return "%s(%s)"%(self.user.first_name, self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "专业负责人"

@receiver(post_save, sender=PM, dispatch_uid="创建之后要自动添加至专业负责人组")
def add_pm_group(sender, instance=None, created=False, **kwargs):
    if created:
        group, b = Group.objects.get_or_create(name="专业负责人")
        instance.user.groups.add(group)

class Squad(models.Model):
    name = models.CharField("班级名", max_length=50)
    created_year = models.IntegerField("年级")
    tutor = models.ForeignKey(Tutor, models.SET_NULL, "squads", verbose_name="导员", null=True, blank=True)

    def __str__(self):
        return f"{self.created_year}级 {self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "班级"


class Student(models.Model):
    user = models.OneToOneField(User, models.CASCADE, "username", verbose_name="账户", primary_key=True)
    squad = models.ForeignKey(Squad, models.SET_NULL, "students", verbose_name="班级", null=True)
    admission_date = models.DateField(verbose_name="入学日期")
    graduation_date = models.DateField(verbose_name="毕业日期")
    length_of_schooling = models.IntegerField(default=4, verbose_name="学制")
    field_of_study = models.ForeignKey(
        FieldOfStudy, models.SET_NULL,
        null=True, blank=True,
        related_name="students", verbose_name="专业方向"
    )

    def __str__(self):
        return "%s(%s)"%(self.user.first_name, self.user.username)

    class Meta:
        verbose_name = verbose_name_plural = "学生"

@receiver(post_save, sender=Student, dispatch_uid="创建之后要自动添加至学生组")
def add_student_group(sender, instance=None, created=False, **kwargs):
    if created:
        group, b = Group.objects.get_or_create(name="学生")
        instance.user.groups.add(group)