from django.contrib import admin

# Register your models here.
from polls.models import Question

# 注册自定义模块
admin.site.register(Question)
