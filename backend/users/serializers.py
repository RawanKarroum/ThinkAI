from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    """
    Serializer for Users model
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        
        fields = [
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'full_name', 
        ]
        read_only_fields = ['full_name']

    def get_full_name(self, obj):
        """
        Return the full name of the user by combining first and last name.
        """
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_role(self, value):
        """
        Check if the role is valid
        """
        if value not in dict(Users.ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role")
        return value

    def validate(self, attrs):
        """
        Check if email is valid
        """
        if attrs.get('email') and not attrs.get('email').endswith('@example.com'):
            raise serializers.ValidationError({'email': "Email must end with '@example.com'."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user
        """
        return Users.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing user
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
