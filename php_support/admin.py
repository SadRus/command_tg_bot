from django.contrib import admin
from .models import Client, Devman, Task, Status


class ClientTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'client'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )
    extra = 0


class DevmanTasksInline(admin.TabularInline):
    model = Task
    fk_name = 'devman'
    fields = (
        'title',
        'status',
    )
    readonly_fields = ('title', )
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('username', 'user_id')
    readonly_fields = ('username', 'user_id')
    list_editable = ('is_access', )
    list_filter = ('is_access', )
    list_display = [
        'username',
        'is_access',
        'user_id',
    ]
    inlines = [ClientTasksInline]

class DevmanAdmin(admin.ModelAdmin):
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