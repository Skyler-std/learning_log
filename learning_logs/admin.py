from django.contrib import admin
from .models import Topic, Entry

# 更改后台内容
admin.site.site_header = '学习笔记管理后台'
admin.site.site_title = '学习笔记管理后台'
admin.site.index_title = '学习笔记管理后台'

admin.site.register(Topic)
admin.site.register(Entry)
