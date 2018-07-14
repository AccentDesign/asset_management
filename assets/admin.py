from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from assets.models import *


class TaskInline(admin.StackedInline):
    extra = 0
    model = Task
    readonly_fields = [
        'last_due',
        'next_due'
    ]

class AssetAdmin(MPTTModelAdmin):
    inlines = [
        TaskInline,
    ]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetType)
admin.site.register(Manufacturer)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'asset',
        'last_due',
        'next_due'
    ]
    readonly_fields = [
        'last_due',
        'next_due'
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskType)
