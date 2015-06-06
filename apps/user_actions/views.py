from rest_framework import viewsets
from rest_framework import permissions

from apps.user_actions.serializers import DoneSerializer, BookmarkSerializer, ViewSerializer, ShareSerializer, ReviewSerializer
from apps.user_actions.models import Done, Bookmark, View, Share, Review

"""
API Endpoint for user_actions module
"""


class UserActionPermission(permissions.BasePermission):
    """
    Permission granted as follows-
    Create: Allow any authenticated user to create
    Read: Any user is allowed to read
    Update: Only the user associated with the model is allowed to update
    Delete: Only the user associated with the model is allowed to delete
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True

        if request.method in ['POST']:
            return obj.user.is_authenticated()

        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.user

        return False


class UserActionAbstractViewSet(viewsets.ModelViewSet):
    permission_classes = (UserActionPermission,)


class DoneViewSet(UserActionAbstractViewSet):
    """
    API endpoint for Done model
    """
    queryset = Done.objects.all()
    serializer_class = DoneSerializer
    
    
class BookmarkViewSet(UserActionAbstractViewSet):
    """
    API endpoint for Bookmark model
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
    
class ViewViewSet(UserActionAbstractViewSet):
    """
    API endpoint for View model
    """
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    
    
class ShareViewSet(UserActionAbstractViewSet):
    """
    API endpoint for Share model
    """
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    
    
class ReviewViewSet(UserActionAbstractViewSet):
    """
    API endpoint for Review model
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer