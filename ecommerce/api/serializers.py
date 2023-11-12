from rest_framework import serializers
from .models import ProductCategory, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.category")

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_name = category_data.get("category")
        category, _ = ProductCategory.objects.get_or_create(category=category_name)

        validated_data["category"] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        try:
            category_data = validated_data.pop("category")
            category_name = category_data.get("category")
            category, _ = ProductCategory.objects.get_or_create(category=category_name)

            validated_data["category"] = category
        except KeyError:
            pass
        return super().update(instance, validated_data)
