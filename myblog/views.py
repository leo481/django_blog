import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


def get_sevendays_hot_data():
    sevendays = timezone.now().date() - datetime.timedelta(days=7)
    blogs = Blog.objects\
                .filter(read_details__date__lt=timezone.now().date(), read_details__date__gte=sevendays)\
                .values('id', 'title')\
                .annotate(read_num_sum=Sum('read_details__read_num'))\
                .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    # cache.clear()
    sevendays_hot_data = cache.get('sevendays_hot_data')
    if sevendays_hot_data is None:
        sevendays_hot_data = get_sevendays_hot_data()
        cache.set('sevendays_hot_data', sevendays_hot_data, 60*60)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['sevendays_hot_data'] = sevendays_hot_data
    return render(request, 'home.html', context=context)

def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)