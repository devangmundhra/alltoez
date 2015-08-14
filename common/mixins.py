# coding=utf-8
# TODO add docstring

from rest_framework import permissions


class UserRequired(object):
    """Mixin to check User is authenticated

    If nor user is not authenticated HTTP 401 UNAUTHORIZED will raise
    """
    permission_classes = (permissions.IsAuthenticated, )