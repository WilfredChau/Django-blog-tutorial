from django.contrib import admin
from .models import Category, Tag, Post

# 在这里注册写好的模型


# 该类用于令后台文章列表展示页显示更详细的信息
# list_display属性控制Post列表页展示的字段
# fields属性控制表单展示的字段
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    # 这里的save_model方法是复写ModelAdmin中的方法，且覆写其中的save_model方法
    # 该方法第一个参数为request即此次HTTP请求对象，第二个为obj即此次创建的关联对象的实例
    # 覆写save_model方法，令request.user关联到创建的Post实例上
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
