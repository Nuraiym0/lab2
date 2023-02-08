from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from drf_yasg.utils import swagger_auto_schema


from .serializers import CommentSerializer, RatingSerializer#, LikeDiselikeComentSerializer
from .models import Comment, Rating, LikeDiselikeComent

from main.permissions import IsAuthorOrReadOnly


User = get_user_model()

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(['PUT'], detail=True)
    def like(self, request, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        comment = get_object_or_404(Comment, id=pk)

        if LikeDiselikeComent.objects.filter(comment=comment, user=user).exists():
            LikeDiselikeComent.objects.filter(comment=comment, user=user).delete()
        else:
            LikeDiselikeComent.objects.create(comment=comment, user=user)

        return Response(status=201)



class CreateRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RatingSerializer())
    def post(self, request):
        user = request.user
        ser = RatingSerializer(data=request.data, context={"request":request})
        ser.is_valid(raise_exception=True)
        course_id = request.data.get("rating")
        if Rating.objects.filter(author=user, course__id=course_id).exists():
            raiting = Rating.objects.get(author=user, course__id=course_id) 
            raiting.value = request.data.get("value")
            raiting.save()
        else:
            ser.save()
        return Response(status=201)
