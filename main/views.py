from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Profile, Archive, Order, Course, Category, CourseItem, CourseItemFile
from .serializers import ProfileSerializer, ArchiveSerializer, OrderSerializer, CourseSerializer, CategorySerializer, CourseItemSerializer, CourseItemFileSerializer
from .permissions import IsMentor, IsAuthorOrReadOnly


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            return [IsAuthorOrReadOnly()]
        return [IsMentor()]

    
    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset() 
        if q:
            queryset = queryset.filter(Q(title__icontains=q))

        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            return [IsAuthorOrReadOnly()]
        return [IsMentor()]

    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset() 
        if q:
            queryset = queryset.filter(Q(title__icontains=q))

        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ArchiveViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseItemViewSet(ModelViewSet):
    queryset = CourseItem.objects.all()
    serializer_class = CourseItemSerializer


class CourseItemFileViewSet(ModelViewSet):
    queryset = CourseItemFile.objects.all()
    serializer_class = CourseItemFileSerializer