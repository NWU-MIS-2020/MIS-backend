from django.contrib import admin
from django.db.models import Q

from .models import RoughRequirement, DetailedRequirement, IndicatorFactor, FieldOfStudy, OfferingCourse, BasisTemplate

# Register your models here.

@admin.register(RoughRequirement)
class RoughRequirementAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'description')
    list_display_links = ('index', 'title')

@admin.register(DetailedRequirement)
class DetailedRequirementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    list_filter = ('rough_requirement',)

    def name(self, obj):
        return obj
    name.short_description = '序号'


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
            return queryset.filter(Q(field_of_study__id=self.value())|Q(field_of_study__id=None))

@admin.register(IndicatorFactor)
class IndicatorFactorAdmin(admin.ModelAdmin):
    list_display = ('detailed_requirement', 'offering_course', 'field_of_study', "factor")
    list_display_links = ('detailed_requirement', 'offering_course', 'field_of_study')

    list_filter = (FieldOfStudyListFilter, 'detailed_requirement', 'offering_course')
    

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(OfferingCourse)
class OfferingCourseAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'course_type', "course_property", "credit", "total_period", "semester")
    list_display_links = ('number', 'name')
    list_filter = ('course_type', "course_property", "semester")

@admin.register(BasisTemplate)
class BasisTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator_factor', 'name', 'full_marks')