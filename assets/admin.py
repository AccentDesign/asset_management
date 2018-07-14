from django.contrib import admin

from assets.models import *


admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Manufacturer)
admin.site.register(Task, list_display=('__str__', 'asset', 'last_due', 'next_due'))
admin.site.register(TaskType)
