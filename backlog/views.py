from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewSprint, NewBackLog, NewTask

# Create your views here.
from .models import BackLog, Sprint, Task


def home(request):
    backlogs = BackLog.objects.all()
    li =[]

    for backlog in backlogs:
        counter = 0
        for sprint in backlog.sprints.all():
            counter += sprint.tasks.all().count()
        li.append(counter)
    return render(request, 'home.html', {'backlogs': backlogs, 'li': li})


def count(request, pk):
    backlog = get_object_or_404(BackLog, pk=pk)
    counter = 0
    for sprint in backlog.sprints.all.count():
        counter += sprint.tasks.all.count()
    return render(request, 'home.html', {'counter': counter})


def backlog_sprints(request, pk):
    backlog = get_object_or_404(BackLog, pk=pk)
    return render(request, 'sprint.html', {'backlog': backlog})


def sprint_tasks(request, pk, spk):
    backlog = get_object_or_404(BackLog, pk=pk)
    sprint = get_object_or_404(Sprint, pk=spk)
    return render(request, 'task.html', {'backlog': backlog, 'sprint': sprint})


def new_sprint(request, pk):
    backlog = get_object_or_404(BackLog, pk=pk)
    if request.method == 'POST':
        sprint = Sprint.objects.create(
            name=request.POST['name'],
            backlog=backlog,
            end_at=request.POST['dead_line']
        )
        return redirect('backlog_sprints', pk=backlog.pk)
    return render(request, 'new_sprint.html', {'backlog': backlog, 'form': NewSprint})


def new_task(request, pk, spk):
    backlog = get_object_or_404(BackLog, pk=pk)
    sprint = get_object_or_404(Sprint, pk=spk)
    if request.method == 'POST':
        task = Task.objects.create(
            name=request.POST['name'],
            sprint=sprint,
            description=request.POST['description'],
            end_at=request.POST['dead_line'],
            importance=request.POST['importance'],

        )
        return redirect('sprint_tasks', pk, spk)
    return render(request, 'new_task.html', {'backlog': backlog, 'sprint': sprint, 'form': NewTask})


def new_backlog(request):
    if request.method == 'POST':
        backlog = BackLog.objects.create(
            name=request.POST['name'],
            end_at=request.POST['dead_line'],
        )
        return redirect('home')
    return render(request, 'new_backlog.html', {'form': NewBackLog})


def sprint_tasks(request, pk, spk):
    backlog = get_object_or_404(BackLog, pk=pk)
    sprint = get_object_or_404(Sprint, pk=spk)
    return render(request, 'task.html', {'backlog': backlog, 'sprint': sprint})
