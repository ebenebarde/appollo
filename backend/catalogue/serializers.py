from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'bio']


class AlbumListSerializer(serializers.ModelSerializer):
    """
    Lightweight version for list views (e.g., "All Albums").
    Here we do NOT load all tracks to preserve performance.
    """
    artist = serializers.StringRelatedField() 

    class Meta:
        model = Album
        fields = ['id', 'title', 'slug', 'artist', 'release_date', 'genre']


class AlbumTrackSerializer(serializers.ModelSerializer):
    """
    A lightweight version of the Track WITHOUT album data.
    Used ONLY within AlbumDetailSerializer to avoid redundancy.
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
    Detailed version for the detailed view of an album.
    Here we include the tracks (Nested Serializer).
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
            'tracks',  
        ]