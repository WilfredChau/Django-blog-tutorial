from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.


# 创建Category数据表，表中字段name数据类型为CharField字符型，最大长度100
class Category(models.Model):
    # 分类名
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # Meta类用于使blog应用下的模型名在后台显示为中文
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


# Tag表
class Tag(models.Model):
    # 标签名
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # Meta类用于使blog应用下的模型名在后台显示为中文
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


# 文章表相对复杂，设计字段title body created_time modified_time excerpt
# 此外还有category tags两个字段为关联Category和Tag表的字段
class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文
    body = models.TextField('正文')

    # 文章摘要，可为空
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 创建时间和最新修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')  # 修改时间不能用的default，因为有默认值后第二次保存的值不起作用

    # 关联外部表字段，分类名和标签名
    # CASCADE参数为级联删除，表示当一个分类被删除，分类下全部文章被删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 文章作者
    # User表为django内置的用户模型，该字段逻辑与category相似
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # Meta类用于使blog应用下的模型名在后台显示为中文
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # 覆写save方法，在model被save到数据库前指定modified_time的值为当前时间
    # 实现每次保存模型时，都修改modified_time的值
    # 在数据被把保存到数据库前，先从body字段摘取n个字符保存到excerpt中,从而实现自动摘要
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 实例化一个Markdown类用于渲染body文本
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 将markdown本文渲染成html文本
        # strip_tags方法去掉html文本的全部标签
        # 从文本摘取前54个字符给excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # reverse函数第一个参数表示blog应用下名为detail的函数
        # 勇敢reverse函数来获取对应的网址
        return reverse('blog:detail', kwargs={'pk': self.pk})
