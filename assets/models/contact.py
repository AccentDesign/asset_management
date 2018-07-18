from django.db import models
from django.urls import reverse_lazy


class Contact(models.Model):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('assets:contact-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
