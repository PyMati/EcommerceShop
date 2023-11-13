from rest_framework import serializers
from .models import ProductCategory, Product, Order, Address
from PIL import Image
import os


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.category")

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {"thumbnail": {"required": False}}

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_name = category_data.get("category")
        category, _ = ProductCategory.objects.get_or_create(category=category_name)
        validated_data["category"] = category

        image_data = validated_data.get("image")
        try:
            thumbnail = Image.open(image_data).convert("RGB")
            thumbnail.thumbnail((200, 200), Image.LANCZOS)
            thumbnail_path = f"thumbnails/{validated_data['name']}_thumbnail.jpg"
            thumbnail.save(thumbnail_path)
            validated_data["thumbnail"] = thumbnail_path
        except (IOError, OSError) as e:
            print(f"Cannot create thumbnail: {e}")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        category_data = validated_data.get("category")
        if category_data:
            category_name = category_data.get("category")
            category, _ = ProductCategory.objects.get_or_create(category=category_name)
            validated_data["category"] = category

        image_data = validated_data.get("image")
        if image_data:
            try:
                thumbnail = Image.open(image_data).convert("RGB")
                thumbnail.thumbnail((200, 200), Image.LANCZOS)
                path = instance.thumbnail.path
                thumbnail.save(path)
                validated_data["thumbnail"] = path
                os.remove(instance.image.path)
                print("Thumbnail created")
            except (IOError, OSError) as e:
                print(f"Cannot create thumbnail: {e}")

        return super().update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class OrderSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    address = AddressSerializer()
    products = serializers.JSONField()

    def create(self, validated_data, summary, today, payment_date, price, client_id):
        address = validated_data.get("address")
        address_id, _ = Address.objects.get_or_create(**address)
        new_order = Order.objects.create(
            client=client_id,
            delivery_address=address_id,
            ordered_products_summary=summary,
            order_date=today,
            payment_date=payment_date,
            price=price,
        )


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
