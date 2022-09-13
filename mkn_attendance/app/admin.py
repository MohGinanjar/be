from django.contrib import admin
from .models import ListProject, ProjectDescription

# Register your models here.
admin.site.register(ListProject)


@admin.register(ProjectDescription)
class ProjectDescriptionAdmin(admin.ModelAdmin):
    list_display = ['emp','date','choice_project','detail_project','status']