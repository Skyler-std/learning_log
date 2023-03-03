from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """主页"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """主题列表"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {
        'topics': topics
    }
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示每个主题的笔记"""
    topic = Topic.objects.get(id=topic_id)
    if not check_topic_owner(topic, request):
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """新建主题"""
    if request.method != 'POST':
        # 未提交数据, 创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # 表单有效,即检查包含了所有的有效字段
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    # 显示空表单或者指出表单无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """新建笔记"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # 未使用post方法
        form = EntryForm()
    else:
        # post提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # 显示空表单或者指出表单无效
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑笔记"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if not check_topic_owner(topic, request):
        raise Http404
    
    if request.method != 'POST':
        # 初次请求：使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # post提交的数据：进行数据处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(topic, request):
    """检查主题拥有者"""
    if topic.owner != request.user:
        return False
    return True
