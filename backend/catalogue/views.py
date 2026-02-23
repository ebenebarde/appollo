from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Artist, Album, Track
from .serializers import (
    ArtistSerializer, 
    AlbumListSerializer, 
    AlbumDetailSerializer, 
    TrackSerializer
)

class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for artists.
    Allows: GET /artists/ (list) and GET /artists/{slug}/ (detail).
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'           


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for albums.
    Allows: GET /albums/ (list) and GET /albums/{slug}/ (detail).
    """
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Optimized database queries to avoid the N+1 problem.
        """
        queryset = Album.objects.all()

        if self.action == 'retrieve':
            return queryset.select_related('artist').prefetch_related('tracks')
        
        return queryset.select_related('artist')

    def get_serializer_class(self):
        """
        Handle different serializers for list vs. detail views.
        """
        if self.action == 'retrieve':
            return AlbumDetailSerializer 
        return AlbumListSerializer


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for individual tracks.
    Allows: GET /tracks/{slug}/
    """
    queryset = Track.objects.select_related('album__artist').all()
    serializer_class = TrackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'