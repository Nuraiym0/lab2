from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, default="")
    competence = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    site_url = models.TextField()
    twitter_url = models.TextField(verbose_name='Twitter')
    facebook_url = models.TextField(verbose_name='Facebook')
    linkedin_url = models.TextField()
    youtube_url = models.TextField(verbose_name='Youtube')
    image = models.ImageField(upload_to='media', null=True, blank=True, default="")
    is_hidden = models.BooleanField(default=False)
    is_hidden_course = models.BooleanField(default=False)
    promotions = models.BooleanField(default=False)
    mentor_ads = models.BooleanField(default=False)
    email_ads = models.BooleanField(default=True)


    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Category(models.Model):
    title = models.CharField(max_length=255)


class Course(models.Model):
    user_id = models.ForeignKey(User, related_name='course', on_delete=models.CASCADE)
    categoty_id = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField()
    lang = models.CharField(max_length=20, choices=[('english', 'английский'), ('russian', 'русский'), ('kyrgyz', 'кыргызский')])
    level = models.CharField(max_length=20, choices=[('beginner', 'начинающий'), ('advanced', 'продвинутый'), ('professional', 'профи')])
    sub_category = models.IntegerField()
    image_show = models.ImageField(upload_to='media', null=True, blank=True, default="")
    video = models.FileField()
    price = models.DecimalField(max_digits=10, decimal_places=2)



class Order(models.Model):
    user_id = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE, )
    course_id = models.ForeignKey(Course, related_name='order', on_delete=models.CASCADE)


class Archive(models.Model):
    user_id = models.ForeignKey(User, related_name='archive', on_delete=models.CASCADE, )
    course_id = models.ForeignKey(Course, related_name='archive', on_delete=models.CASCADE)



class CourseItem(models.Model):
    course_id = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()


class CourseItemFile(models.Model):
    course_item_id = models.ForeignKey(Course, related_name='course_item', on_delete=models.CASCADE)
    file = models.FileField()

    
