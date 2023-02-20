from rest_framework import serializers

from .models import Profile, Archive, Order, Category, Course, CourseItem, CourseItemFile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields= ['language', 'image']

    # def to_representation(self, instance):
    #     return super().to_representation(instance)



class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Archive
        fields= ['__all__']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields= ['__all__']

    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields= ['__all__']


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['course'] = CourseSerializer(instance.course).data
        
        return rep


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields= ['__all__']


    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


    def to_representation(self, instance: Course):
        rep = super().to_representation(instance)
        rep['rating'] = instance.rating
        rep['comment'] = instance.comment
        rep['order'] = instance.order
        rep['archive'] = instance.archive
        return rep


class CourseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseItem
        fields= ['__all__']


class CourseItemFileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseItemFile
        fields= ['__all__']


