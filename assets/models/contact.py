from django.db import models
from django.urls import reverse_lazy


class ContactManager(models.Manager):
    def search(self, query=None):
        """ Returns the search results for the main site search """

        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                models.Q(name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Contact(models.Model):
    name = models.CharField(
        max_length=255
    )

    objects = ContactManager()

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('assets:contact-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
