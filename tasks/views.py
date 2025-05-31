from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    total_count = tasks.count()
    completed_count = tasks.filter(completed=True).count()
    pending_count = tasks.filter(completed=False).count()
    
    # 進捗率を計算
    completion_rate = round((completed_count / total_count) * 100) if total_count > 0 else 0
    
    context = {
        'tasks': tasks,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'completion_rate': completion_rate,
    }
    return render(request, 'tasks/task_list.html', context)

def task_create(request):
    print(f"task_create view called with method: {request.method}")
    
    if request.method == 'POST':
        print("Processing POST request")
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'タスク「{task.title}」を作成しました。')
            print(f"Task created: {task.title}")
            return redirect('task_list')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'フォームに入力エラーがあります。確認してください。')
    else:
        print("Creating new form")
        form = TaskForm()
    
    print("Rendering form template")
    return render(request, 'tasks/task_form.html', {'form': form})

def task_test(request):
    return HttpResponse("Test view is working!")

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'タスク「{task.title}」を更新しました。')
            return redirect('task_list')
        else:
            messages.error(request, 'フォームに入力エラーがあります。確認してください。')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'タスク「{task_title}」を削除しました。')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})