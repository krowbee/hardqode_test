from rest_framework import serializers
from .models import Product, Lesson, Viewing

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ViewingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewing
        fields = '__all__'

class LessonInfoSerializer(serializers.Serializer):
    lesson = serializers.CharField()
    status = serializers.BooleanField()
    timestamp = serializers.IntegerField()