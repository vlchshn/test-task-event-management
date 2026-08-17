from __future__ import annotations

from typing import ClassVar

from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    ATTENDEE_ACTIONS: ClassVar[set[str]] = {"register"}

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action in self.ATTENDEE_ACTIONS:
            return True

        return obj.organizer == request.user
