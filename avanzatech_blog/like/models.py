from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel
from like.constants import LIKE_STATUS
from user.models import CustomUser
from post.models import Post


class Like(BaseModel):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    LIKE_STATUS_CHOICES = [(status, description) for (status, description) in LIKE_STATUS.items()]
    status = models.CharField(max_length=10, choices=LIKE_STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if self.status not in LIKE_STATUS.keys():
            raise ValueError(_("Invalid Status"))

        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(post) + str(user)
