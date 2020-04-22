from django.contrib import admin

from plan.models import FieldOfStudy

from .models import Student, Teacher, Tutor, CM, PM, Squad

# Register your models here.

class FieldOfStudyListFilter(admin.SimpleListFilter):
    title = "专业方向"
    parameter_name = "field_of_study"

    def lookups(self, request, model_admin):
        fields = FieldOfStudy.objects.all()
        yield ("未分类", "未分类")
        for field in fields:
            yield (field.id, field.name)

    def queryset(self, request, queryset):
        if self.value() is None:
            return None
        if self.value() == "未分类":
            return queryset.filter(field_of_study=None)
        else:
            return queryset.filter(field_of_study__id=self.value())

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'field_of_study')
    list_filter = (FieldOfStudyListFilter, )
    def name(self, obj):
        return obj.user.first_name
    name.short_description = '姓名'
    def username(self, obj):
        return obj.user.username
    username.short_description = '工号'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    def name(self, obj):
        return obj.user.first_name
    name.short_description = '姓名'
    def username(self, obj):
        return obj.user.username
    username.short_description = '工号'

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    def name(self, obj):
        return obj.user.first_name
    name.short_description = '姓名'
    def username(self, obj):
        return obj.user.username
    username.short_description = '工号'

@admin.register(CM)
class CMAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    def name(self, obj):
        return obj.user.first_name
    name.short_description = '姓名'
    def username(self, obj):
        return obj.user.username
    username.short_description = '工号'

@admin.register(PM)
class PMAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    def name(self, obj):
        return obj.user.first_name
    name.short_description = '姓名'
    def username(self, obj):
        return obj.user.username
    username.short_description = '工号'

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_year', 'tutor')
