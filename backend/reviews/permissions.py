from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom Permission: Erlaubt nur dem Besitzer eines Objekts, dieses zu bearbeiten.
    Alle anderen dürfen nur lesen (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Leserechte sind für alle erlaubt (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Schreibrechte nur für den Besitzer des Objekts (obj.user)
        return obj.user == request.user