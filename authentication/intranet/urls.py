from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet, ChatViewSet, 
    ChatMemberViewSet, MessageViewSet, NotificationViewSet, 
    ContactViewSet, BlockListViewSet, SeenViewSet, UserStatusViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'chat-members', ChatMemberViewSet, basename='chat-member')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'blocklist', BlockListViewSet, basename='blocklist')
router.register(r'seen', SeenViewSet, basename='seen')
router.register(r'status', UserStatusViewSet, basename='status')

urlpatterns = router.urls
