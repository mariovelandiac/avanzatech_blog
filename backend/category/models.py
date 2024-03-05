from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name
