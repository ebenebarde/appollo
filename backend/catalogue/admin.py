from django.contrib import admin
from .models import Album, Artist, Track

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__name')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('artist', 'release_date')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'album', 'position', 'average_rating', 'review_count')
    search_fields = ('title', 'album__title', 'album__artist__name')
    list_filter = ('album',)
    ordering = ('album', 'position')