from django.contrib.admin.utils import NestedObjects
from django.db import router


class ProtectedDeleteMixin:

    def _get_protected(self):
        using = router.db_for_write(self.object)
        collector = NestedObjects(using=using)
        collector.collect([self.object])

        def callable_func(obj):
            meta = obj._meta
            data = {
                'object': obj,
                'verbose_name': obj._meta.verbose_name,
                'has_permission': self.request.user.has_perm('%s.delete_%s' % (meta.app_label, meta.model_name))
            }
            return data

        return [callable_func(o) for o in collector.protected]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'protected': self._get_protected()
        })
        return context
