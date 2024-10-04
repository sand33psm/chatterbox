from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_chats",  blank=True)
    rechats = models.ManyToManyField(User, related_name="rechats", blank=True)
    reply_count = models.PositiveBigIntegerField(default=0)
    attachments = models.FileField(upload_to="chats/", blank=True, null=True)
    is_public = models.BooleanField(default=True)

    def like_count(self):
        return self.likes.count()

    def rechats_count(self):
        return self.rechats.count()

    def __str__(self):
        return f'Chat by {self.user.username}: {self.text[:80]}'

class Rechat(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
        
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)


