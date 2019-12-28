from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from .serializers import BlogSerializer, UserSerializer
from blog.models import Blog
from .permissions import IsOwnerOrReadOnly

class BlogList(generics.ListCreateAPIView):
    """
    List all blogs, or create a new blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'blogs': reverse('blog-list', request=request, format=format)
    })

from rest_framework import renderers

class BlogContent(generics.GenericAPIView):
    queryset = Blog.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        return Response(blog.content)


# ================== 使用viewset ===================

from rest_framework import viewsets
from rest_framework.decorators import action

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def contenthtml(self, request, *args, **kwargs):
        blog = self.get_object()
        return Response(blog.content)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
