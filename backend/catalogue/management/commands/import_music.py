import os
import requests
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from catalogue.models import Artist, Album, Track

class Command(BaseCommand):
    help = 'Seeds the database with specific albums from the Spotify API.'

    def get_spotify_token(self):
        """
        Authenticates with Spotify API using Client Credentials flow.
        """
        client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('Spotify credentials missing in environment variables.'))
            return None

        auth_url = 'https://accounts.spotify.com/api/token'
        try:
            response = requests.post(auth_url, {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
            }, timeout=5)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to get Spotify token: {e}'))
            return None

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting Spotify data seed...'))
        
        token = self.get_spotify_token()
        if not token:
            return

        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        album_ids = [
            "41GuZcammIkupMPKH2OJ6I", # ASTROWORLD
            "4yP0hdKOZPNshxUOjY0cZj", # After Hours
            "2QRedhP5RmKJiJ1i8VgDGR", # Whole Lotta Red
            "58iEeJbYd6OBGRM0TiwltL", # A Great Chaos
            "3mH6qwIy9crq0I9YQbOuDf", # Blonde
            "4eLPsYPBmXABThSJ821sqY", # DAMN.
            "4g1ZRSobMefqF6nelkgibi", # Hollywood's Bleeding
            "20r762YmB5HeofjMCiPMLv", # My Beautiful Dark Twisted Fantasy
            "7mgdTKTCdfnLoa1HXHvLYM", # Lil Uzi Vert vs. The World
            "5JpH5T1sCYnUyZD6TM0QaY", # Cry Baby
        ]

        ids_string = ','.join(album_ids)
        api_url = f"https://api.spotify.com/v1/albums?ids={ids_string}"

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            with transaction.atomic():
                self.process_albums(data.get('albums', []))
                
            self.stdout.write(self.style.SUCCESS('Successfully seeded 10 albums from Spotify!'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'API Request failed: {e}'))

    def process_albums(self, albums_data):
        """
        Maps Spotify JSON responses to our Django models.
        """
        for album_data in albums_data:
            if not album_data:
                continue

            # 1. Process Artist (using the primary artist)
            primary_artist_data = album_data['artists'][0]
            artist, _ = Artist.objects.get_or_create(
                name=primary_artist_data['name'],
                defaults={'bio': ''} 
            )

            # 2. Process Album
            # Handle potentially incomplete release dates (e.g., just '1993' instead of '1993-09-21')
            release_date_str = album_data.get('release_date')
            release_date = None
            if release_date_str:
                if len(release_date_str) == 4:
                    release_date = f"{release_date_str}-01-01"
                elif len(release_date_str) == 7: 
                    release_date = f"{release_date_str}-01"
                else:
                    release_date = release_date_str

            album, _ = Album.objects.get_or_create(
                artist=artist,
                title=album_data['name'],
                defaults={
                    'release_date': release_date,
                    'genre': album_data['genres'][0] if album_data.get('genres') else ''
                }
            )

            # 3. Process Tracks
            for track_data in album_data['tracks']['items']:
                duration_ms = track_data.get('duration_ms', 0)
                duration_td = datetime.timedelta(milliseconds=duration_ms)

                Track.objects.update_or_create(
                    album=album,
                    position=track_data['track_number'],
                    defaults={
                        'title': track_data['name'],
                        'duration': duration_td
                    }
                )