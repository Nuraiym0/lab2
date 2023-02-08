from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Archive, Order, Category, Course, CourseItem, CourseItemFile

from review.models import Comment, Rating, LikeDiselikeComent


class RatingInline(admin.TabularInline):
    model = Rating


class CommentInline(admin.TabularInline):
    model = Comment

class LikeDiselikeComentInLine(admin.TabularInline):
    model = LikeDiselikeComent


class ArchiveLine(admin.TabularInline):
    model = Archive


class OrderLine(admin.TabularInline):
    model = Order


class CategoryAdmin(admin.ModelAdmin):
    list_display =['title']


class CourseItemAdmin(admin.ModelAdmin):
    list_display =['title', 'description']


class CourseItemFileAdmin(admin.ModelAdmin):
    list_display = ['file']



class CourseAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'categoty_id', 'title', 'sub_title', 'description', 'lang', 'level', 'sub_category', 'image_show', 'video', 'price']
    # list_filter = ['category',]

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = 'image'



admin.site.register(Archive)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseItem ,CourseItemAdmin)
admin.site.register(CourseItemFile, CourseItemFileAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(LikeDiselikeComent)







