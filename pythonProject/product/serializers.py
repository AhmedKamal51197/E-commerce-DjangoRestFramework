from rest_framework import serializers
from .models import Product,Reviews
class ProductSerializer(serializers.ModelSerializer):
    reviews =  serializers.SerializerMethodField(method_name='get_reviews',read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
    def get_reviews(self,obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"

