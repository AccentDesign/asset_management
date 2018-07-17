from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from assets.models import *


class AssetAdmin(MPTTModelAdmin):
    list_display = [
        '__str__',
        'task_count'
    ]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetType)
admin.site.register(Manufacturer)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'asset',
        'last_due',
        'last_completed',
        'next_due'
    ]
    readonly_fields = [
        'last_due',
        'last_completed',
        'next_due'
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCompletion)
admin.site.register(TaskType)
