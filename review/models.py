from django.db import models
from django.contrib.auth import get_user_model

from main.models import Course


User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

class Rating(models.Model):
    user_id = models.ForeignKey(User, related_name='raiting', on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, related_name='raiting', on_delete=models.CASCADE)
    value = models.CharField(max_length=20, choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])


class LikeDiselikeComent(models.Model):
    user_id = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    course_id = models.ForeignKey(User, related_name='course_like', on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)
