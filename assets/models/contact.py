from django.db import models
from django.urls import reverse_lazy

from .mixins import CollectionManager, CollectionMixin


class ContactManager(CollectionManager):
    def search(self, query=None):
        """ Returns the search results for the main site search """

        qs = self.get_queryset()
        if query:
            all_filters = models.Q()
            for term in query.split():
                or_lookup = (
                    models.Q(name__icontains=term) |
                    models.Q(email__icontains=term) |
                    models.Q(phone_number__icontains=term) |
                    models.Q(mobile_number__icontains=term) |
                    models.Q(address__icontains=term) |
                    models.Q(url__icontains=term) |
                    models.Q(notes__icontains=term)
                )
                all_filters = all_filters & or_lookup
            qs = qs.filter(all_filters).distinct()
        return qs


class Contact(CollectionMixin):
    name = models.CharField(
        max_length=255
    )
    email = models.EmailField(
        blank=True
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True
    )
    mobile_number = models.CharField(
        max_length=20,
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    url = models.URLField(
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    for_collection = ContactManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('assets:contact-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    @property
    def google_maps_link(self):
        return """<a href="https://www.google.co.uk/maps/search/{}" target="_blank">Google Maps</a>""".format(
            self.address.replace(' ', '+').replace('\n', '+')
        )
