from collections import OrderedDict
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from .views import CourseViewSet
from .models import Course
from book.models import User


class PostTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(
            email='test@gmail.com',
            password='12345678'
        )

        posts = [
            Course(author = user, title = '1 post', description = '11'),
            Course(author = user, title = '2 post', description = '22'),
            Course(author = user, title = '3 post', description = '33'),
        ]        
        Course.objects.bulk_create(posts)


    def test_listing(self):
        request = self.factory.get('/posts/')
        view = CourseViewSet.as_view({'get':'list'})
        response = view(request)

        assert response.status_code == 200
        assert len(response.data) == 3
        assert type(response.data) == ReturnList
        assert type(response.data[0]) == OrderedDict
        assert response.data[0]['title'] == '1 post'


    def test_details(self):
        post = Course.objects.first()
        request = self.factory.get(f'/posts/{post.id}/')
        view = CourseViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=post.id)

        assert response.status_code == 200
        assert type(response.data) == ReturnDict
        assert response.data['title'] == '1 post'


    def test_permissions(self):
        data ={
            'title':'4 post',
        }
        request = self.factory.post('/posts/', data, format='json')
        view = CourseViewSet.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 401

    
    def test_create(self):
        user = User.objects.first()
        data = {
            'title':'4 post'
        }
        request = self.factory.post('/posts/', data, format='json')
        force_authenticate(request, user)
        view = CourseViewSet.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 201
        assert Course.objects.filter(
            author=user, 
            title='4 post', 
            description='').exists()

