from django.contrib import admin
from .models import Profile, Chat, ChatMember, Message, UserStatus, BlockList, Seen, Contact, Notification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'online_status', 'bio']  # Adjust to use existing fields
    search_fields = ['user__username', 'online_status', 'bio']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'member_count', 'created_by', 'created_at']
    search_fields = ['name', 'type', 'created_by__username']
    list_filter = ['type', 'created_at']


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'user', 'role', 'is_muted', 'joined_at']
    search_fields = ['chat__name', 'user__username', 'role']
    list_filter = ['role', 'is_muted']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'sender', 'content', 'timestamp', 'is_delivered', 'is_read']
    search_fields = ['chat__name', 'sender__username', 'content']
    list_filter = ['message_type', 'timestamp']

    # Helper functions to show read/delivered status
    def is_read(self, obj):
        return obj.read_at is not None
    is_read.boolean = True
    is_read.short_description = 'Read'

    def is_delivered(self, obj):
        return obj.delivered_at is not None
    is_delivered.boolean = True
    is_delivered.short_description = 'Delivered'


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'current_status', 'expires_at', 'visibility']
    search_fields = ['user__username', 'current_status', 'visibility']
    list_filter = ['visibility', 'expires_at']


@admin.register(BlockList)
class BlockListAdmin(admin.ModelAdmin):
    list_display = ['id', 'blocker', 'blocked', 'created_at']
    search_fields = ['blocker__username', 'blocked__username']
    list_filter = ['created_at']


@admin.register(Seen)
class SeenAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'seen_at']
    search_fields = ['message__content', 'user__username']
    list_filter = ['seen_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'contact', 'is_favorite', 'added_at']
    search_fields = ['user__username', 'contact__username']
    list_filter = ['is_favorite', 'added_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'type', 'is_read', 'created_at']
    search_fields = ['user__username', 'content', 'type']
    list_filter = ['type', 'is_read', 'created_at']
