from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# 存放视图函数


# 首页的视图函数
# render函数作用为结合一个给定的模板和一个给定的上下文字典，返回一个渲染后的HttpResponse对象
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 详情页的视图函数
def detail(request, pk):
    # 当传入的pk对应的Post在数据库中存在时，就返回对应的pk，若不存在，返回404错误，表示请求不存在
    post = get_object_or_404(Post, pk=pk)
    # 解析Markdown，将Markdown文本转为HTML文本再传递给模板
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    # 用正则匹配生成目录中包裹在ul标签中的内容，如非空，说明有目录，将ul标签中的值提取出来，赋值给post.toc，否则post的toc为空字符串
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


# 归档页面视图函数
def archive(request, year, month):
    # 利用filter方法来进行条件过滤
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类页面视图函数
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 标签页面视图函数
def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})