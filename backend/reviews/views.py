from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews.
    Allows: GET /reviews/ (list), POST /reviews/ (create), GET /reviews/{id}/ (detail),
    PUT/PATCH /reviews/{id}/ (update), DELETE /reviews/{id}/ (delete).
    """
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        return Review.objects.select_related('user', 'track').order_by('-created_at')
