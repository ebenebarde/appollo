from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):
    """
    Wandelt Artist-Modelle in JSON um.
    """
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio']


class AlbumListSerializer(serializers.ModelSerializer):
    """
    Leichtere Version für Listenansichten (z.B. "Alle Alben").
    Hier laden wir NICHT alle Tracks, um die Performance zu schonen.
    """
    artist = serializers.StringRelatedField() 

    class Meta:
        model = Album
        fields = ['id', 'title', 'slug', 'artist', 'release_date', 'genre']


class AlbumTrackSerializer(serializers.ModelSerializer):
    """
    NEU: Eine schlanke Version des Tracks OHNE Album-Daten.
    Wird NUR innerhalb von AlbumDetailSerializer verwendet, 
    um Redundanz zu vermeiden.
    """
    class Meta:
        model = Track
        fields = [
            'id', 
            'position', 
            'title', 
            'slug', 
            'duration',
            'average_rating',
            'review_count'
        ]


class TrackSerializer(serializers.ModelSerializer):
    """
    Standard Track Serializer.
    """
    album = AlbumListSerializer(read_only=True)

    class Meta:
        model = Track
        fields = ['id', 'title', 'album', 'position', 'slug', 'duration', 'average_rating', 'review_count']


class AlbumDetailSerializer(serializers.ModelSerializer):
    """
    Detaillierte Version für die Einzelansicht eines Albums.
    Hier inkludieren wir die Tracks (Nested Serializer).
    """
    artist = ArtistSerializer(read_only=True)
    tracks = AlbumTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            'id', 
            'title', 
            'slug', 
            'artist', 
            'release_date',
            'genre',
            'tracks',   # Das hier ist das Feld, das durch Zeile 61 gefüllt wird
        ]