from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import (
    Profile, Chat, ChatMember, Message, 
    UserStatus, Contact, Notification, 
    BlockList, Seen
)
from intranet.serializers import (
    UserSerializer, ProfileSerializer, 
    ChatSerializer, ChatMemberSerializer, 
    MessageSerializer, UserStatusSerializer, 
    ContactSerializer, NotificationSerializer, 
    BlockListSerializer, SeenSerializer
)

# ------------------------------------------
# 🔹 User and Profile Views
# ------------------------------------------

class UserViewSet(ReadOnlyModelViewSet):
    """Read-only view for users"""
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class ProfileViewSet(ModelViewSet):
    """CRUD operations for the Profile model"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only allow users to access their own profile"""
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure the user cannot update someone else's profile"""
        serializer.save(user=self.request.user)


# ------------------------------------------
# 🔹 Chat, Chat Members, and Message Views
# ------------------------------------------

class ChatViewSet(ModelViewSet):
    """ViewSet for creating, listing, and managing Chats"""
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only chats the user is a member of"""
        return self.queryset.filter(members__user=self.request.user)

    def perform_create(self, serializer):
        """Set the creator of the chat automatically"""
        serializer.save(created_by=self.request.user)


class ChatMemberViewSet(ModelViewSet):
    """ViewSet for managing Chat Members"""
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only allow access to chat members where the user is a member"""
        return self.queryset.filter(chat__members__user=self.request.user)


class MessageViewSet(ModelViewSet):
    """ViewSet for sending and retrieving Messages"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return messages in chats the user is a member of"""
        return self.queryset.filter(chat__members__user=self.request.user)

    def perform_create(self, serializer):
        """Set the sender of the message automatically"""
        serializer.save(sender=self.request.user)


# ------------------------------------------
# 🔹 Notification and Contact Views
# ------------------------------------------

class NotificationViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing Notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notifications for the current user"""
        return self.queryset.filter(user=self.request.user)


class ContactViewSet(ModelViewSet):
    """ViewSet for managing user's contacts"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return contacts for the current user"""
        return self.queryset.filter(user=self.request.user)


# ------------------------------------------
# 🔹 Block List and Seen Views
# ------------------------------------------

class BlockListViewSet(ModelViewSet):
    """ViewSet for managing block list"""
    queryset = BlockList.objects.all()
    serializer_class = BlockListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only show the block list of the current user"""
        return self.queryset.filter(blocker=self.request.user)

    def perform_create(self, serializer):
        """Set the current user as the blocker"""
        serializer.save(blocker=self.request.user)


class SeenViewSet(ModelViewSet):
    """ViewSet for tracking when users have seen a message"""
    queryset = Seen.objects.all()
    serializer_class = SeenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return seen records for messages in chats the user is part of"""
        return self.queryset.filter(message__chat__members__user=self.request.user)

    def perform_create(self, serializer):
        """Set the user for the 'seen' record automatically"""
        serializer.save(user=self.request.user)


# ------------------------------------------
# 🔹 User Status Views
# ------------------------------------------

class UserStatusViewSet(ModelViewSet):
    """ViewSet for creating, updating, and retrieving user statuses"""
    queryset = UserStatus.objects.all()
    serializer_class = UserStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return user status entries for the current user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the status is linked to the current user"""
        serializer.save(user=self.request.user)

