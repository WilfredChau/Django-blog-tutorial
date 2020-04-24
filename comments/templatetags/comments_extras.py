from django import template
from ..forms import CommentForm

# 该文件用于存放comments应用下自定义的模板标签代码


register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }