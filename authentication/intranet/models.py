from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    online_status = models.CharField(max_length=20, choices=[
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('busy', 'Busy'),
    ], default='offline')
    



class Chat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # For group chats
    description = models.TextField(blank=True)
    group_picture = models.ImageField(upload_to='group_pics/', null=True, blank=True)
    CHAT_TYPE_CHOICES = [
    ('private', 'Private'),
    ('group', 'Group'),]
    type = models.CharField(max_length=10, choices=CHAT_TYPE_CHOICES, default='private')
    member_count = models.PositiveIntegerField(default=0)
    is_typing = models.BooleanField(default=False)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_chats')




class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
    ('member', 'Member'),
    ('admin', 'Admin'),
    ('owner', 'Owner'),]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    is_muted = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('location', 'Location')
    ], default='text')
    media_file = models.FileField(upload_to='chat_media/', null=True, blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_forwarded = models.BooleanField(default=False)
    reactions = models.JSONField(default=dict, blank=True)  # Stores data like {'👍': 3, '❤️': 5}
    expires_at = models.DateTimeField(null=True, blank=True)




class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_status = models.CharField(max_length=100)
    story_text = models.CharField(max_length=255, null=True, blank=True, default="")
    image = models.ImageField(upload_to='status_images/', null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    visibility = models.CharField(max_length=20, choices=[
    ('everyone', 'Everyone'),
    ('contacts', 'My Contacts'),
    ('custom', 'Custom'),
    ], default='contacts')




class BlockList(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    created_at = models.DateTimeField(auto_now_add=True)




class Seen(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='seen_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message', 'user']),
        ]


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_contacted_by')
    is_favorite = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[
        ('message', 'Message'),
        ('invite', 'Group Invite'),
        ('status', 'Status Update'),
    ], default='message')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
