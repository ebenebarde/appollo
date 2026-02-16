from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review

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
            count=Count('id')
        )
        new_average = aggregates['average_rating']
        new_count = aggregates['count']
        
        # Sicherstellen, dass wir runden und Defaults setzen
        track.average_rating = round(new_average, 1) if new_average is not None else 0.0
        track.review_count = new_count if new_count is not None else 0
    else:
        # Keine Reviews mehr vorhanden (z.B. letztes gelöscht)
        track.average_rating = 0.0 
        track.review_count = 0
        
    # Performance-Pflicht erfüllt: Nur die geänderten Felder speichern!
    track.save(update_fields=['average_rating', 'review_count'])