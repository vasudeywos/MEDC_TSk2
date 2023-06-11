from django.db import models
from users.models import User

class Message(models.Model):
    room_name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')
    content = models.TextField(blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False)

    def __str__(self):
        return self.author.username

    def load_messages(self):
        return Message.object.order_by('-timestamp').all()
