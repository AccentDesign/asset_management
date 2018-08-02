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
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Status)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'asset',
        'last_due',
        'last_completed',
        'next_due',
        'due_date',
    ]
    readonly_fields = [
        'last_due',
        'last_completed',
        'next_due',
        'due_date',
    ]


admin.site.register(Task, TaskAdmin)


class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'task',
        'date',
        'user',
        'status'
    ]
    readonly_fields = [
        'date',
        'user'
    ]


admin.site.register(TaskHistory, TaskHistoryAdmin)
admin.site.register(TaskPriority)
admin.site.register(TaskType)
