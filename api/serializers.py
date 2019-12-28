from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Blog, BlogType


# class BlogSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=True, max_length=100)
#     # content = serializers.CharField(style={'base_template': 'textarea.html'})
#     content = serializers.CharField()
#     author = serializers.CharField()
#     created_time = serializers.DateTimeField(read_only=True)
#     last_updated_time = serializers.DateTimeField(read_only=True)


#     def create(self, validated_data):
#         """
#         根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
#         """
#         return Blog.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    blog_type = serializers.PrimaryKeyRelatedField(queryset=BlogType.objects.all())
    contenthtml = serializers.HyperlinkedIdentityField(view_name='blog-contenthtml', format='html')
    class Meta:
        model = Blog
        fields = ['url', 'title', 'blog_type', 'content', 'contenthtml', 'author', 'created_time', 'last_updated_time']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.HyperlinkedRelatedField(many=True, view_name='blog-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'blogs']