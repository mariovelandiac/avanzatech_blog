from django.db import models
from team.constants import DEFAULT_TEAM_NAME
# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True, default=DEFAULT_TEAM_NAME)

    def __str__(self):
        return self.name