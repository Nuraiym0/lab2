from rest_framework.serializers import ModelSerializer

from .models import Comment, Rating, LikeDiselikeComent


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user
        return attrs


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        return rep


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['author'] = request.user

        return attrs


class LikeDiselikeComentSerializer(ModelSerializer):
    class Meta:
        model = LikeDiselikeComent
        fields = ('__all__')
