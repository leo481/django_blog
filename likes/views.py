from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikesRecord, LikesCount

# Create your views here.


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(likes_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['likes_num'] = likes_num
    return JsonResponse(data)

def likes_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        likes_record, created = LikesRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            likes_count, created = LikesCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            likes_count.likes_num += 1
            likes_count.save()
            return SuccessResponse(likes_count.likes_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'already liked')
    else:
        # 要取消点赞
        if LikesRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            likes_record = LikesRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            likes_record.delete()
            # 点赞总数减1
            likes_count, created = LikesCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                likes_count.likes_num -= 1
                likes_count.save()
                return SuccessResponse(likes_count.likes_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'already unliked')