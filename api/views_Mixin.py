from rest_framework import mixins
from rest_framework import generics
from .serializers import BlogSerializer
from blog.models import Blog
   

class BlogList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    List all blogs, or create a new blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BlogDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a code blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
