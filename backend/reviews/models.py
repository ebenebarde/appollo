from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.forms import ValidationError
from catalogue.models import Track

def validate_rating_step(value):
    if value % Decimal('0.5') != 0:
        raise ValidationError('Das Rating muss in 0,5er Schritten erfolgen.')

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')), 
            MaxValueValidator(Decimal('10.0')),
            validate_rating_step
        ],
        null=True, blank=True 
    )
    
    text_content = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'track')

    def clean(self):
        if self.rating is None and not self.text_content:
            raise ValidationError("A review must have either a rating or text content.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username} for {self.track.title}"
    
    
@receiver([post_save, post_delete], sender=Review)
def update_track_rating(sender, instance, **kwargs):
    """
    Wird ausgeführt, sobald ein Review gespeichert oder gelöscht wird.
    Berechnet den Durchschnitt aller Reviews für den betroffenen Track neu.
    """
    track = instance.track
    reviews = track.reviews.all()
    
    if reviews.exists():

        aggregates = reviews.aggregate(
            average_rating=Avg('rating'),
            count=models.Count('id')
        )
        new_average = aggregates['average_rating']
        new_count = aggregates['count']
        
        track.average_rating = round(new_average, 1) if new_average is not None else 0.0
        track.review_count = new_count if new_count is not None else 0
    else:
        # Keine Reviews mehr vorhanden
        track.average_rating = 0.0 
        track.review_count = 0
        
    track.save(update_fields=['average_rating', 'review_count'])