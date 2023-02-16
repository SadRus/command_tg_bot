from django.contrib import admin
from php_support.models import Client, Devman, Task, Status


#class ClientAdmin(admin.ModelAdmin):

admin.site.register(Client)
admin.site.register(Devman)
admin.site.register(Task)
admin.site.register(Status)