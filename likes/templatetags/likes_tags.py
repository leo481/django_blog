from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikesCount, LikesRecord

register = template.Library()

@register.simple_tag
def get_likes_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    likes_count = LikesCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)[0]
    return likes_count.likes_num

@register.simple_tag(takes_context=True)
def get_likes_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikesRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''