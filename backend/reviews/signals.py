from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def update_track_rating(sender, instance, **kwargs):
    """
    Executed after a review is created, updated, or deleted.
    It recalculates the average rating and review count for the associated track.
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
        
        track.average_rating = round(new_average, 1) if new_average is not None else 0.0
        track.review_count = new_count if new_count is not None else 0
    else:
        track.average_rating = 0.0 
        track.review_count = 0
        
    track.save(update_fields=['average_rating', 'review_count'])