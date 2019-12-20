from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_info/', views.user_info, name='user_info'),
    path('modify_nickname/', views.modify_nickname, name='modify_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code', views.send_verification_code, name='send_verification_code'),
    path('send_reg_verification_code', views.send_reg_verification_code, name='send_reg_verification_code'),
    path('modify_password', views.modify_password, name='modify_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
]