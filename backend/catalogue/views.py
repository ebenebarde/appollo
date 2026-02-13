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
    API-Endpoint für Künstler.
    Erlaubt: GET /artists/ (Liste) und GET /artists/{slug}/ (Detail).
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny] # Öffentlich zugänglich
    lookup_field = 'slug'           # Wir nutzen Slugs statt IDs in der URL


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API-Endpoint für Alben.
    Erlaubt: GET /albums/ (Liste) und GET /albums/{slug}/ (Detail).
    """
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Optimierte Datenbank-Abfragen zur Vermeidung des N+1 Problems.
        """
        queryset = Album.objects.all()

        if self.action == 'retrieve':
            # Detailansicht: Wir brauchen Tracks und Artist.
            # 'select_related' für den Artist (ForeignKey)
            # 'prefetch_related' für die Tracks (Reverse ForeignKey / One-to-Many)
            return queryset.select_related('artist').prefetch_related('tracks')
        
        # Listenansicht: Wir brauchen nur den Artist (für den Namen im Serializer)
        return queryset.select_related('artist')

    def get_serializer_class(self):
        """
        Wählt dynamisch den richtigen Serializer basierend auf der Aktion.
        """
        if self.action == 'retrieve':
            return AlbumDetailSerializer  # Enthält Trackliste & Description
        return AlbumListSerializer        # Schlanke Version für Listen


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API-Endpoint für einzelne Tracks.
    Erlaubt: GET /tracks/{slug}/
    """
    queryset = Track.objects.select_related('album__artist').all()
    serializer_class = TrackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'