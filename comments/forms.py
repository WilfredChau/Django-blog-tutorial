from django import forms
from .models import Comment


# 编写评论表单代码


# 一张表单对应一个模型
class CommentForm(forms.ModelForm):

    # 内部类指定一些和表单相关的内容
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

