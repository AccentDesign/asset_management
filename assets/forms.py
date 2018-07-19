from django.forms import inlineformset_factory

from assets.models import Asset, Task


AssetTaskFormset = inlineformset_factory(
    Asset,
    Task,
    exclude=('asset', ),
    extra=0,
    can_delete=False,
    can_order=False
)
