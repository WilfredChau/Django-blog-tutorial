from django.urls import path
from . import views

# 绑定URL
app_name = 'comments'
urlpatterns = [
    # 配置评论页面URL
    path('comment/<int:post_pk>', views.comment, name='comment')
]