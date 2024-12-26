from rest_framework import serializers

from product.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer handles the conversion of Category model instances
    to and from JSON format, as well as field-level validation for the
    'name' field.

    Methods:
        validate_name: Ensures the category name has at least 3 characters.
    """

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        """
        Field-level validation for the 'name' field.

        Ensures the category name has at least 3 characters.
        Raises a ValidationError if the condition is not met.

        Args:
            value (str): The value of the 'name' field to validate.

        Returns:
            str: The validated name value.

        Raises:
            serializers.ValidationError: If the name is less than 3 characters.
        """
        if len(value) <= 0:
            raise serializers.ValidationError(
                "Category name must be at least 3 characters long"
            )
        return value
