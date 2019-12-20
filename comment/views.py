from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

# Create your views here.

def update_comment(request):
    # user = request.user    
    # text = request.POST.get('text', '').strip()
    # if text == '':
    #     return render(request, 'error.html', {'message': '评论内容不能为空'})

    # content_type = request.POST.get('content_type', '')
    # object_id = request.POST.get('object_id', '')
    # try:
    #     ct = ContentType.objects.get(model=content_type)
    # except Exception:
    #     return render(request, 'error.html', {'message': '评论对象不存在'})

    # # model_class = ContentType.objects.get(model=content_type).model_class()
    # # model_instance = model_class.objects.get(pk=object_id)
    # comment = Comment(text=text, user=user, content_type=ct, object_id=object_id)
    # comment.save()

    # referer = request.META.get('HTTP_REFERER', '/')
    # return redirect(referer)

    referer = request.META.get('HTTP_REFERER', '/')
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_type = comment_form.cleaned_data['model_class']
        comment.object_id = comment_form.cleaned_data['object_id']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        
         # 发送邮件通知
        comment.send_mail()
        
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
        # return render(request, 'error.html', {'meesage':comment_form.errors, 'redirect_to': referer})