from django.contrib import admin
from .models import User

admin.site.register(User)


# from django.contrib import admin
# from .models import Blog

# class AdminBlog(admin.ModelAdmin):
#     list_display = ['title', 'language', 'status']

# admin.site.register(Blog,AdminBlog )