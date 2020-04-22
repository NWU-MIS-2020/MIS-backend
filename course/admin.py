from django.contrib import admin

from .models import Course, Grade

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
    list_display = ("student", "course", "final_marks", "indicator")
    list_filter = ("course", "student")