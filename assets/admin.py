from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from reversion.admin import VersionAdmin

from assets.models import *


class AssetAdmin(VersionAdmin, MPTTModelAdmin):
    change_list_template = 'admin/mptt_reversion_change_list.html'


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetFile, VersionAdmin)
admin.site.register(AssetType, VersionAdmin)
admin.site.register(Contact, VersionAdmin)
admin.site.register(Status, VersionAdmin)


class TaskAdmin(VersionAdmin):
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


class TaskHistoryAdmin(VersionAdmin):
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
admin.site.register(TaskPriority, VersionAdmin)
admin.site.register(TaskType, VersionAdmin)
