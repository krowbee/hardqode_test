from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на владельца продукта
    def __str__(self):
        return self.name
    

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    products = models.ManyToManyField(Product, related_name='lessons')  # Уроки могут находиться в нескольких продуктах

    def __str__(self):
        return self.title
    

# Сущность Просмотр
class Viewing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_time_seconds = models.PositiveIntegerField()  # Время просмотра в секундах
    status = models.BooleanField(default=False)  # Статус "Просмотрено" (True) или "Не просмотрено" (False)

    def __str__(self):
        return f"Просмотр урока '{self.lesson.title}' пользователем {self.user.username}"
    

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Lesson, Viewing
from .serializers import ProductSerializer, LessonSerializer, ViewingSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ViewingViewSet(viewsets.ModelViewSet):
    queryset = Viewing.objects.all()
    serializer_class = ViewingSerializer

    # Реализация логики для определения статуса "Просмотрено" на основе времени просмотра
    def perform_create(self, serializer):
        lesson = serializer.validated_data['lesson']
        user = serializer.validated_data['user']
        viewed_time = serializer.validated_data['viewed_time_seconds']
        duration = lesson.duration_seconds

        if (viewed_time / duration) >= 0.8:
            serializer.validated_data['status'] = True

        serializer.save()