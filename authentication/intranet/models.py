from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True)

class Chat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # For group chats
    is_group_chat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_chats')

class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('location', 'Location')
    ], default='text')
    media_file = models.FileField(upload_to='chat_media/', null=True, blank=True)

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_status = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)