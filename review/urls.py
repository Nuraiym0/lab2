from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, CreateRatingAPIView#, LikeDiselikeComent


router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('raiting', CreateRatingAPIView)



urlpatterns = [
    path('', include(router.urls)),
    path('rating/', CreateRatingAPIView.as_view()),
]