from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # 首页URL配置
    path('', views.index, name='index'),
    # 详情页URL配置
    path('posts/<int:pk>/', views.detail, name='detail'),
    # 归档页面URL配置
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    # 分类页面URL配置
    path('categories/<int:pk>/', views.category, name='category'),
    # 标签页面URL配置
    path('tags/<int:pk>', views.tag, name='tag'),
]
