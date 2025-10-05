from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Notification(models.Model):
    user            = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    message         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    read            = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user}: {self.message[:50]}"