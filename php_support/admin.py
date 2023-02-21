from django.contrib import admin
from .models import Client, Devman, Task, Status

from import_export.admin import ExportMixin


class ClientTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'client'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )
    extra = 0


@admin.register(Client)
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

    @admin.display(description='Всего задач')
    def tasks_count(self, obj):
        return obj.tasks.count()


class DevmanTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'devman'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )
    extra = 0


@admin.register(Devman)
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
    
    @admin.display(description='Всего задач')
    def tasks_count(self, obj):
        return obj.tasks.count()


@admin.register(Task)
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


admin.site.register(Status)
