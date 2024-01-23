from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel
from common.constants import STATUS, STATUS_CHOICES
from user.models import CustomUser
from post.models import Post

class Comment(BaseModel):

    content = models.TextField(blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
 
        if not self.user:
            raise ValueError(_("Invalid User"))

        if not self.post:
            raise ValueError(_("Invalid Post"))

        if not self.content:
            raise ValueError(_("Invalid Content"))

        if self.status not in STATUS.keys():
            raise ValueError(_("Invalid_status"))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment {self.id} by {self.user.username}"