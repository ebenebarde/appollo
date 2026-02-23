# catalogue/models.py
import uuid
from django.db import models
from django.db import IntegrityError
from django.utils.text import slugify

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.artist.name}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.artist.name})"

class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(help_text="Nummer auf dem Album")

    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.album.artist.name}-{self.title}")
            self.slug = base_slug
            
            if Track.objects.filter(slug=self.slug).exists():
                 if not self.pk or Track.objects.get(pk=self.pk).slug != self.slug:
                    self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        
        super().save(*args, **kwargs)
        

    class Meta:
        ordering = ['position']
        unique_together = ('album', 'position')

    def __str__(self):
        return f"{self.position}. {self.title}"