from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, OrderViewSet, CourseViewSet, ArchiveViewSet, CategoryViewSet, CourseItemViewSet, CourseItemFileViewSet
from . import views

router = DefaultRouter()

router.register('profile', ProfileViewSet)
router.register('profile', OrderViewSet)
router.register('profile', CourseViewSet)
router.register('profile', ArchiveViewSet)
router.register('profile', CategoryViewSet)
router.register('profile', CourseItemViewSet)
router.register('profile', CourseItemFileViewSet)


urlpatterns =[
    path('', include(router.urls)),
    # path('history/', views.history, name='history'),
    # path('', views.index, name='index.html'),
]
