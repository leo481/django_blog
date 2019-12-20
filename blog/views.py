from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read
from .models import Blog, BlogType

# Create your views here.

def blog_list(request):
    page_num = request.GET.get('page', 1)
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page_of_blogs = paginator.get_page(page_num)
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginator.num_pages]

    context = {}
    # context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render(request, 'blog/blog_list.html', context=context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=content_type, object_id=blog.pk, parent=None)

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    # context['comments'] = comments.order_by('-comment_time')
    # data = dict(content_type=content_type, object_id=blog_pk, reply_comment_id=0)
    # context['comment_form'] = CommentForm(initial=data)
    # context['comment_count'] = Comment.objects.filter(content_type=content_type, object_id=blog.pk).count()
    # context['login_form'] = LoginForm()
    response = render(request, 'blog/blog_detail.html', context=context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    page_num = request.GET.get('page', 1)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs, 5)
    page_of_blogs = paginator.get_page(page_num)
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginator.num_pages]

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render(request, 'blog/blogs_with_type.html', context=context)

def blogs_with_date(request, year, month):
    context = {}

    return render(request, 'blog/blogs_with_type.html', context=context)