from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.mixin import ReadNumMixin
from read_statistics.models import ReadDetail

# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumMixin):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '<Blog: {}>'.format(self.title)

    class Meta:
        ordering = ['-created_time']

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def get_user(self):
        return self.author
    