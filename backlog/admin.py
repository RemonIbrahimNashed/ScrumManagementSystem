from django.contrib import admin

# Register your models here.
from backlog.models import BackLog, Sprint

admin.site.register(BackLog)
admin.site.register(Sprint)