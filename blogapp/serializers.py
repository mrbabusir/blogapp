from rest_framework import serializers
from .models import *
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

# User = get_user_model

# class UserSerializer(serializers.Serializer):
#    class Meta:
#       model = User
#       fields = ['id','username','email']

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = [ 'id','category_name']  # category ko sabai field haru lai include gareko
      
   def save(self, **kwargs): #creating save function for the new category 
      validated_data = self.validated_data
      samecategory_count = self.Meta.model.objects.filter(category_name=validated_data['category_name']).count() 
      if samecategory_count > 0 :
         raise serializers.ValidationError ('Category Already Exists.')
      categorylist = Category(**validated_data)
      categorylist.save()
      return categorylist
      

class CommentSerializer(serializers.ModelSerializer):
   username = serializers.CharField(source='user.username', read_only=True)
   class Meta:
      model = Comment
      fields = ['id','post_id','comment','user','username','dateandtime'] # comment ko sabai field haru lai include gareko
      read_only_fields = ('id','dateandtime','user','username')

class CommentDetailSerializer(serializers.ModelSerializer):
   username = serializers.CharField(source='user.username', read_only=True)
   title = serializers.CharField(source='post_id.title', read_only=True)  # comment ma blog ko title lai include gareko
   class Meta:
      model = Comment
      fields = ['id','title','comment','user','username','dateandtime']
      read_only_fields = ['id','user','username','dateandtime']


class BlogListSerializer(serializers.ModelSerializer):
   username = serializers.CharField(source = 'user.username', read_only = True)
   category = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all(),required=False) # blog detail ma category ko serializer lai include gareko
   class Meta:
      model = Blog
      fields = ['id','title','blogcontent','category','user','username','dateandtime']
      read_only_fields = ('id', 'user', 'dateandtime','username')
   def create(self, validated_data):
        categories = validated_data.pop('category', []) ##create garda categories ma 
        blog = Blog.objects.create(**validated_data)
        if categories:
            blog.category.set(categories)     
        return blog


class BlogDetailSerializer(serializers.ModelSerializer): #blog detail ko lagi serializer banako
   username = serializers.CharField(source='user.username', read_only=True)#field ma username dekhauna banako
   email = serializers.EmailField(source = 'user.email',read_only = True)#field ma email dekhauna banako
   category = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all(),required=False) # blog detail ma category ko serializer lai include gareko
   comments = CommentSerializer(many=True, read_only=True) # comments ko serializer lai blog detail ma include gareko
   class Meta:
      model = Blog
      fields = ['id','title','blogcontent','category','user','username','email','dateandtime','comments'] # blog detail ma sabai field haru lai include gareko
      read_only_fields = ['id','user','username','email','dateandtime','comments']
class CategoryDetailSerializer(serializers.ModelSerializer):
   blogs = BlogListSerializer(many=True, read_only=True)  # category ma blog ko list lai include gareko
   class Meta:
      model = Category
      fields = ['id', 'category_name', 'blogs']

