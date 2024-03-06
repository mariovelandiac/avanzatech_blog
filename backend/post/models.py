from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.constants import READ_PERMISSIONS, EXCERPT_LENGTH
from user.models import CustomUser
from category.models import Category
from permission.models import Permission



class Post(BaseModel):

    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    excerpt = models.CharField(max_length=200, null=False, default="")
    READ_PERMISSIONS_CHOICES = [(key,value) for (key,value) in READ_PERMISSIONS.items()]
    read_permission = models.CharField(
        max_length=20, choices=READ_PERMISSIONS_CHOICES, default='public')

    def save(self, *args, **kwargs):
        if self.read_permission not in list(READ_PERMISSIONS.keys()):
            raise ValueError(_('Invalid Permission'))

        if not self.title:
            raise ValueError(_('Title must be set'))

        if not self.content:
            raise ValueError(_('Content must be set'))

        self.excerpt = self.content[:EXCERPT_LENGTH] if len(self.content) > EXCERPT_LENGTH else self.content
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

class PostCategoryPermission(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')


