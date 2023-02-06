from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from enum import Enum

from .tasks import send_activation_code

User = get_user_model()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # self.model == User
        user:User = self.model(email=email, **kwargs)
        user.set_password(password) # хеширует пароль
        user.create_activation_code()
        user.save(using=self._db) # сохраняем в бд
        send_activation_code.delay(user.email, user.activation_code)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs['is_active'] = False # false for google
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_active'] = True
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create(email, password, **kwargs)


class MentorTypeEnum(Enum):
    a = 'лично, частным образом'
    b = 'лично, профессионально'
    c = 'онлайн'
    d = 'другое'

class MentorExperienceEnum(Enum):
    yes = 'да'
    no = 'нет'


class MentorAudienceEnum(Enum):
    a = 'в настоящий момент нет'
    b = 'у меня маленькая аудитория'
    c = 'у меня достаточная аудитория'

   


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)
    # type = models.ForeignKey(MentorTypeEnum, related_name='type', on_delete=models.CASCADE, default="")
    # experience = models.ForeignKey(MentorExperienceEnum, related_name='experience', on_delete=models.CASCADE, default="")
    # audience = models.ForeignKey(MentorAudienceEnum, related_name='audience', on_delete=models.CASCADE, default="")
                #  choices=[(tag, tag.value) for tag in BlogStatus]
    type = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in MentorTypeEnum]) 
    experience = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in MentorExperienceEnum]) 
    audience = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in MentorAudienceEnum]) 
    is_mentor = models.BooleanField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def create_activation_code(self):
        self.activation_code = get_random_string(8, 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



# class Profile(AbstractUser):
#     user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, default="")
#     competence = models.CharField()
#     language = models.CharField()
#     site_url = models.TextField()
#     twitter_url = models.TextField(verbose_name='Twitter')
#     facebook_url = models.TextField(verbose_name='Facebook')
#     linkedin_url = models.TextField()
#     youtube_url = models.TextField(verbose_name='Youtube')
#     image = models.ImageField(upload_to='media', null=True, blank=True, default="")
#     is_hidden = models.BooleanField()
#     is_hidden_course = models.BooleanField()
#     promotions = models.BooleanField()
#     mentor_ads = models.BooleanField()
#     email_ads = models.BooleanField()


