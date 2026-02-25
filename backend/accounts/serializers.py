from django.contrib.auth import get_user_model
from rest_framework import serializers

# Get the custom user model defined in settings (accounts.User)
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for reading user data (Profile view).
    Excludes sensitive data like passwords.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'slug', 'date_joined')
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Ensures password is not returned in response and is hashed correctly.
    Uses the project's custom User model.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        """
        Check that passwords match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        The custom User model handles slug generation in its save() method.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
