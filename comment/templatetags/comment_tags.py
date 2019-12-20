from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return comment_count

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = dict(content_type=content_type, object_id=obj.pk, reply_comment_id=0)
    comment_form = CommentForm(initial=data)
    return comment_form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    comments = comments.order_by('-comment_time')
    return comments