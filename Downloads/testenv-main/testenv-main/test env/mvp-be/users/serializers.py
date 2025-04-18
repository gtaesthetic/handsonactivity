from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},  # Make these optional
            "last_name": {"required": False}
        }

    def create(self, validated_data):
        # During registration, we'll allow creating employee accounts
        # For manager accounts, we'll set them to inactive by default
        is_manager = validated_data.get("role") == "manager"
        if is_manager:
            validated_data['is_active'] = False  # Managers need admin approval

        # Ensure Administrator accounts are active by default
        is_admin = validated_data.get("role") == "admin"
        if is_admin:
            validated_data['is_active'] = True

        user = User.objects.create_user(**validated_data)
        return user
