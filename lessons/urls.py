from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'all_lessons', views.LessonViewSet)
router.register(r'viewings', views.ViewingViewSet)
#router.register(r'my_lessons',views.LessonListView,basename="my-lessons")


urlpatterns = [
    path('', include(router.urls)),
]