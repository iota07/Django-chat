from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Chat, ChatMember, Message, UserStatus, Contact, 
    Notification, BlockList, Seen
)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model (basic user info)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model"""
    user = UserSerializer(read_only=True)  # Embed User details

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'profile_picture', 'online_status']


class ChatMemberSerializer(serializers.ModelSerializer):
    """Serializer for the ChatMember model"""
    user = UserSerializer(read_only=True)  # Show user details in the response

    class Meta:
        model = ChatMember
        fields = ['id', 'chat', 'user', 'role', 'is_muted', 'joined_at']


class ChatSerializer(serializers.ModelSerializer):
    """Serializer for the Chat model"""
    created_by = UserSerializer(read_only=True)  # Show the creator's user details
    members = ChatMemberSerializer(many=True, read_only=True)  # Nested members details
    last_message = serializers.PrimaryKeyRelatedField(read_only=True)  # Only shows the message ID

    class Meta:
        model = Chat
        fields = [
            'id', 'name', 'description', 'group_picture', 'type', 
            'member_count', 'is_typing', 'last_message', 'created_at', 
            'created_by', 'members'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model"""
    sender = UserSerializer(read_only=True)  # Embed sender details
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Reply messages as a list of IDs
    reactions = serializers.JSONField()  # Show reactions as a JSON object

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'content', 'timestamp', 'delivered_at', 
            'read_at', 'message_type', 'media_file', 'reply_to', 
            'is_forwarded', 'reactions', 'expires_at', 'replies'
        ]


class UserStatusSerializer(serializers.ModelSerializer):
    """Serializer for the UserStatus model"""
    user = UserSerializer(read_only=True)  # Embed user details

    class Meta:
        model = UserStatus
        fields = [
            'id', 'user', 'current_status', 'story_text', 'image', 
            'expires_at', 'visibility'
        ]


class BlockListSerializer(serializers.ModelSerializer):
    """Serializer for the BlockList model"""
    blocker = UserSerializer(read_only=True)  # Embed blocker details
    blocked = UserSerializer(read_only=True)  # Embed blocked user details

    class Meta:
        model = BlockList
        fields = ['id', 'blocker', 'blocked', 'created_at']


class SeenSerializer(serializers.ModelSerializer):
    """Serializer for the Seen model"""
    user = UserSerializer(read_only=True)  # Embed user details
    message = serializers.PrimaryKeyRelatedField(read_only=True)  # Only show message ID

    class Meta:
        model = Seen
        fields = ['id', 'message', 'user', 'seen_at']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for the Contact model"""
    user = UserSerializer(read_only=True)  # Embed user details
    contact = UserSerializer(read_only=True)  # Embed contact user details

    class Meta:
        model = Contact
        fields = ['id', 'user', 'contact', 'is_favorite', 'added_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model"""
    user = UserSerializer(read_only=True)  # Embed user details

    class Meta:
        model = Notification
        fields = ['id', 'user', 'content', 'type', 'is_read', 'created_at']
