from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm

# 存放视图函数


# comment页面视图函数
def comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 构造CommentForm实例，生成一个绑定了用户提交数据的表单
    form = CommentForm(request.POST)

    # 调用form.id_valid()方法，django自动检查表单的数据是否符合格式要求
    if form.is_valid():
        # 检查数据为合法，调用表单的save方法保存数据到数据库
        comment = form.save(commit=False)
        # 将评论与被评论文章相关联
        comment.post = post
        # 保存数据进数据库
        comment.save()
        # 向用户反馈评论成功的消息
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到post详情页
        return redirect(post)

    # 检测数据不合法，渲染一个预览页面表示表单错误
    context = {
        'post': post,
        'form': form,
    }
    # 向用户反馈评论失败的消息
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
