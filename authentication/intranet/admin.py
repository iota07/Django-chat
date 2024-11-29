from django.contrib import admin
from .models import Profile, Chat, ChatMember, Message, UserStatus

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_seen', 'status')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group_chat', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'timestamp', 'is_read')