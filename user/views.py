import string
import random
import hashlib
import datetime
import time
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .forms import LoginForm, RegisterForm, ModifyNicknameForm, BindEmailForm, ModifyPasswordForm, ForgotPasswordForm
from .models import Profile, ConfirmString

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            auth.login(request, login_form.cleaned_data['user'])
            return redirect(request.GET.get('from', '/'))
            
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context=context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        auth.login(request, login_form.cleaned_data['user'])
        data = {}
        data['status'] = 'SUCCESS'
    else:
        data = {}
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', '/'))
            
    else:
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def modify_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ModifyNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile = Profile.objects.get_or_create(user=request.user)[0]
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ModifyNicknameForm()

    context={}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'commonform.html', context)

def hash_code(s, salt='hss'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    # 删除之前的验证码
    if ConfirmString.objects.filter(user=user).exists():
        ConfirmString.objects.filter(user=user).delete()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code

def send_confirm_mail(email, code):
    subject = '来自[黄生生的博客]的注册确认邮件'

    text_content = '''感谢注册黄生生的博客！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>黄生生的博客</a></p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, reverse('confirm'), locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, reverse('bind_email'), locals())
    else:
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, reverse('bind_email'), locals())

def send_verifycode_mail(email, code):
    subject = '来自[黄生生的博客]的邮箱绑定验证码邮件'

    text_content = '''感谢绑定黄生生的博客！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢使用<a href="http://{}/" target=blank>黄生生的博客</a></p>
                    <p>您的验证码是<b>{}</b></p>
                    <p>此验证码有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context={}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request): 
    email = request.GET.get('email', '')
    data = {}
    user = request.user
    if email != '':
        if ConfirmString.objects.filter(user=user).exists():
            ConfirmString.objects.filter(user=user).delete()
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        ConfirmString.objects.create(code=code, user=user)
        send_verifycode_mail(email, code)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def send_reg_verification_code(request): 
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))

        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

            send_verifycode_mail(email, code)
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def modify_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ModifyPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ModifyPasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'commonform.html', context)

def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)