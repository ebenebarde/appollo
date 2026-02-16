from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Review
from catalogue.models import Track
from accounts.models import User


class ReviewUserSerializer(serializers.ModelSerializer):
    """
    Minimalistische Darstellung des Users für öffentliche Reviews.
    Wir wollen nicht das Passwort oder die E-Mail leaken!
    """
    class Meta:
        model = User
        fields = ['id', 'username']
        ref_name = 'ReviewUser'


class ReviewTrackSerializer(serializers.ModelSerializer):
    """
    Minimalistische Darstellung des Tracks.
    """
    class Meta:
        model = Track
        fields = ['id', 'title', 'slug']
        ref_name = 'ReviewTrack'


# --- Main Serializer ---

class ReviewSerializer(serializers.ModelSerializer):
    """
    Der Haupt-Serializer.
    Update zur Architektur: Wir nutzen HiddenField(CurrentUserDefault()),
    damit die Validierung (UniqueTogether) autark im Serializer funktioniert
    und nicht von Logik in der View abhängt.
    """
    
    # HiddenField: Der User wird automatisch aus dem Request Kontext (request.user) geholt.
    # Er ist Teil der validated_data, taucht aber nicht im API-Input Formular auf.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    # Input: ID des Tracks
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
        
        # Hier greift jetzt die Validierung korrekt, da 'user' in den Daten vorhanden ist.
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'track'],
                message="Du hast diesen Song bereits bewertet."
            )
        ]

    def to_representation(self, instance):
        """
        Für die Ausgabe überschreiben wir die Darstellung.
        Statt nichts (HiddenField) oder nur der ID, zeigen wir die User-Details.
        """
        response = super().to_representation(instance)
        
        # Manuelles Nesting für die Ausgabe
        response['user'] = ReviewUserSerializer(instance.user).data
        response['track'] = ReviewTrackSerializer(instance.track).data
        
        return response