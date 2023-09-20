from django.shortcuts import render

# Create your views here

from rest_framework import viewsets, status,generics
from rest_framework.response import Response
from .models import Product, Lesson, Viewing
from .serializers import LessonInfoSerializer, ProductSerializer, LessonSerializer, ViewingSerializer
from rest_framework.permissions import IsAuthenticated

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


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Пример фильтрации уроков по продуктам, к которым у пользователя есть доступ:
        user = self.request.user  # Получаем текущего пользователя
        accessible_products = Product.objects.filter(owner=user)  # Получаем доступные продукты пользователя
        return Lesson.objects.filter(products__in=accessible_products)
    

class LessonListForProductView(generics.ListAPIView):
    serializer_class = LessonInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получите id продукта из URL
        product_id = self.kwargs['product_id']

        # Получите текущего пользователя
        user = self.request.user

        # Найдите продукт по id
        try:
            product = Product.objects.get(id=product_id, owner=user)
        except Product.DoesNotExist:
            # Если продукт с указанным id не найден или не принадлежит пользователю, верните пустой список
            return []

        # Теперь получите уроки, связанные с найденным продуктом
        lessons = Lesson.objects.filter(products=product)

        # Создайте список информации о уроках и их статусе просмотра
        lesson_info = []
        for lesson in lessons:
            try:
                # Получите информацию о просмотре урока пользователем
                viewing = Viewing.objects.filter(lesson=lesson, user=user).latest('id')
                lesson_info.append({
                    'lesson': lesson.title,
                    'status': viewing.status,
                    'timestamp': viewing.viewed_time_seconds,
                })
            except Viewing.DoesNotExist:
                # Если урок не был просмотрен пользователем, создайте запись без просмотра
                lesson_info.append({
                    'lesson': lesson.title,
                    'status': False,
                    'timestamp': None,
                })

        return lesson_info