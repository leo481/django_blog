from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.api_root),
    path('blogs/', views.BlogList.as_view(), name='blog-list'),
    path('blogs/<int:pk>', views.BlogDetail.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/content/', views.BlogContent.as_view(), name='blog-content'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
]

# 添加可选的格式后缀
urlpatterns = format_suffix_patterns(urlpatterns)