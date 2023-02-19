from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count
from .models import Client, Devman, Task, Status

from import_export import fields, resources
from import_export.admin import ImportExportActionModelAdmin, ExportActionMixin, ExportMixin
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field


#client
class ClientResource(resources.ModelResource):

    class Meta:
        model = Client


class ClientTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'client'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )


class ClientAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ('username', 'user_id')
    readonly_fields = ('username', 'user_id')
    list_editable = ('is_access', )
    list_filter = ('is_access', )
    list_display = [
        'username',
        'is_access',
        'user_id',
        'tasks_count'
    ]
    inlines = [ClientTasksInline]
    resource_classes = [ClientResource]

    def tasks_count(self, obj):
        return obj.tasks.count()

#devman
class DevmanResource(resources.ModelResource):

    class Meta:
        model = Devman


class DevmanTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'devman'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )
    extra = 0


class DevmanAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ('username', 'user_id')
    readonly_fields = ('username', 'user_id')
    list_editable = ('is_access', )
    list_filter = ('is_access', )
    list_display = [
        'username',
        'is_access',
        'user_id',
    ]
    inlines = [DevmanTasksInline]
    resource_classes = [DevmanResource]
    
    def tasks_count(self, obj):
        return obj.tasks.count()


#task
class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    readonly_fields = ('client', 'date_start')
    list_editable = ('status', )
    list_filter = ('client', 'status')
    list_display = [
        'title',
        'client',
        'devman',
        'status',
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Devman, DevmanAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Status)