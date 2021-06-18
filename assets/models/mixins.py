import uuid

from django.db import models

from authentication.middleware.current_user import get_current_team


class TeamManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        team = get_current_team()
        if team:
            qs = qs.filter(team=team)
        return qs


class TeamMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    team = models.ForeignKey(
        'authentication.Team',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_team
    )

    class Meta:
        abstract = True
