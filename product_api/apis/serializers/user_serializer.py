from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import CustomUser

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer converts the `User` model instances to and from JSON format.
    It includes all the fields of the user, such as username, email, and any other fields defined in the model.

    Fields:
        - All fields of the user model, such as 'email', 'username', etc.
    """

    class Meta:
        model = user
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used for creating a new user by validating and saving the provided data. It includes password validation
    and ensures that the password is not returned after the user is created.

    Fields:
        - email: The email of the user.
        - username: The username of the user.
        - password: The password of the user (write-only field).

    Methods:
        - create: Creates a new user with the provided email, username, and password.
    """

    password = serializers.CharField(
        write_only=True
    )  # not to return the password after the user is created.

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        This method is called when saving the user instance. It creates a new user with the provided email, username, and password,
        ensuring that the password is hashed.

        Args:
            validated_data (dict): The validated data for the user.

        Returns:
            CustomUser: The newly created user instance.
        """
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
        )
        return user
