from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """主题"""
    text = models.CharField(max_length=200, help_text="主题内容")
    date_added = models.DateTimeField(auto_now_add=True, help_text="添加时间")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = '笔记主题'
        verbose_name_plural = '笔记主题'
    
    def __str__(self):
        """管理页面显示"""
        return self.text

class Entry(models.Model):
    """笔记内容"""
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, help_text="笔记主题", default=4) # 级联删除，外键删除时删除笔记
    text = models.TextField(help_text="笔记内容")
    date_added = models.DateTimeField(auto_now_add=True, help_text="添加时间")
    
    class Meta:
        verbose_name = '笔记内容'
        verbose_name_plural = '笔记内容'
        
    def __str__(self):
        """管理页面显示"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        return f"{self.text}"
    