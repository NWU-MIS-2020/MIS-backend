from django.contrib import admin

from .models import Course, Grade, Basis, IndicatorMark, DetailedMark

# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_description', 'start_date', 'end_date')
    list_display_links = ('id', 'name')
    def name(self, obj):
        return obj.offering_course.name
    name.short_description = '课程名'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "final_marks")
    list_filter = ("course", "student")


@admin.register(Basis)
class BasisAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator_factor', 'course', 'name', 'full_marks')

@admin.register(IndicatorMark)
class IndicatorMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator_factor', 'grade', 'total_marks')
    readonly_fields = ('total_marks',)

@admin.register(DetailedMark)
class DetailedMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator_mark', 'basis', 'marks')
