from itertools import chain
from django.views.generic import ListView

from assets import models


class SearchView(ListView):
    template_name = 'assets/search.html'
    paginate_by = 50
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'count': self.count or 0,
            'query': self.request.GET.get('q')
        })
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            asset_results = models.Asset.objects.search(query)
            contact_results = models.Contact.objects.search(query)
            task_results = models.Task.objects.search(query)
            queryset_chain = chain(
                asset_results,
                contact_results,
                task_results
            )
            qs = sorted(
                queryset_chain,
                key=lambda instance: instance.__str__()
            )
            self.count = len(qs)
            return qs

        return []
