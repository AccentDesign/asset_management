from django.db import models


class Team(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True
    )
    admin = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    members = models.ManyToManyField(
        'authentication.User',
        blank=True,
        related_name='teams'
    )
    guests = models.ManyToManyField(
        'authentication.User',
        blank=True,
        related_name='guested_teams'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title