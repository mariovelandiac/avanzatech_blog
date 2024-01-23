from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from post.constants import READ_PERMISSIONS
from user.models import CustomUser


class Post(BaseModel):

    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    READ_PERMISSIONS_CHOICES = [(key,value) for (key,value) in READ_PERMISSIONS.items()]
    read_permission = models.CharField(
        max_length=20, choices=READ_PERMISSIONS_CHOICES, default=READ_PERMISSIONS['public'])

    def save(self, *args, **kwargs):
        if self.read_permission not in dict(READ_PERMISSIONS):
            raise ValueError(_('Invalid Permission'))

        if self.title is None or self.title == "":
            raise ValueError(_('Title must be set'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


