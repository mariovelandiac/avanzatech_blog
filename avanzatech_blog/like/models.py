from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel
from common.constants import STATUS, STATUS_CHOICES
from user.models import CustomUser
from post.models import Post


class Like(BaseModel):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{str(self.user)} likes the post {str(self.post)}"
        
    class Meta:
        unique_together = ('user', 'post')
        ordering = ["-created_at"]