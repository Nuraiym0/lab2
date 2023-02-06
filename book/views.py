from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, CreateNewPasswordSerializer, UserSerializer
from .models import User


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались", status=201)


class DeleteUserView(APIView):
    def delete(self, request,email):
        user = get_object_or_404(User, email=email)
        print(user)
        print(request.user)
        if user.is_staff or user != request.user:
            return Response(status=403)
        user.delete()
        return Response(status=204) 


class UserListView(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True # activate user
    user.activation_code = '' # delete the activated code
    user.save()
    return Response('Successfuly activated the account', 200)

def send_activation_code(email, activation_code):
    activation_url = f'http://35.185.69.40/account/forgot-password-complete/{activation_code}/'
    message = f"""Чтобы восстановить пароль, пройдите по данной ссылке: {activation_url}"""
    send_mail('Восстановление пароля', message, 'admin@admin.com',recipient_list=[email],)


class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(user.email, user.activation_code)
        return Response('Вам отправлено письмо', status=200)


class ForgotPasswordComplete(APIView):
    @swagger_auto_schema(request_body=CreateNewPasswordSerializer())
    def post(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.activation_code = ''
        serializer = CreateNewPasswordSerializer(data=request.data)
        user.is_active = True
        user.save()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=200)