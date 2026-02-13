from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, AlbumViewSet, TrackViewSet

# Der DefaultRouter erstellt automatisch die URL-Struktur für unsere ViewSets.
# Er generiert auch eine "API Root" Ansicht, die im Browser sehr hilfreich ist.
router = DefaultRouter()

# Wir registrieren unsere Endpunkte.
# Der erste Parameter ist das URL-Präfix, der zweite das ViewSet.
# 'basename' ist optional, da wir ein queryset im ViewSet haben, aber oft gute Praxis.
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'tracks', TrackViewSet, basename='track')

urlpatterns = [
    # Wir inkludieren alle vom Router generierten URLs
    path('', include(router.urls)),
]