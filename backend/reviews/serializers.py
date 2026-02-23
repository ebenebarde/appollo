from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Review
from catalogue.models import Track
from accounts.models import User


class ReviewUserSerializer(serializers.ModelSerializer):
    """
    Minimalistic representation of the User for public reviews.
    We don't want to leak sensitive information here.
    """
    class Meta:
        model = User
        fields = ['id', 'username']
        ref_name = 'ReviewUser'


class ReviewTrackSerializer(serializers.ModelSerializer):
    """
    Minimialistic representation of the Track for public reviews.
    We don't want to leak the full album or artist details here.
    """
    class Meta:
        model = Track
        fields = ['id', 'title', 'slug']
        ref_name = 'ReviewTrack'


# --- Main Serializer ---

class ReviewSerializer(serializers.ModelSerializer):
    """
    The main serializer.
    We use HiddenField(CurrentUserDefault()) so that the validation (UniqueTogether) 
    works independently within the serializer and does not rely on logic in the view.
    """
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())

    class Meta:
        model = Review
        fields = [
            'id', 
            'user', 
            'track', 
            'rating', 
            'text_content', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'track'],
                message="Du hast diesen Song bereits bewertet."
            )
        ]

    def to_representation(self, instance):
        """
        Overriding the representation for output.
        Instead of showing nothing (HiddenField) or just the ID, we display user details.
        """
        response = super().to_representation(instance)
        
        response['user'] = ReviewUserSerializer(instance.user).data
        response['track'] = ReviewTrackSerializer(instance.track).data
        
        return response