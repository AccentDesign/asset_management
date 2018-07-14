from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from assets.models import *


admin.site.register(Asset, MPTTModelAdmin)
admin.site.register(AssetType)
admin.site.register(Manufacturer)
admin.site.register(Task, list_display=('__str__', 'asset', 'last_due', 'next_due'))
admin.site.register(TaskType)
