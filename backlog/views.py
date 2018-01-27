from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewSprint

# Create your views here.
from .models import BackLog, Sprint


def home(request):
    backlogs = BackLog.objects.all()
    return render(request, 'home.html', {'backlogs': backlogs})


def backlog_sprints(request, pk):
    backlog = get_object_or_404(BackLog, pk=pk)
    return render(request, 'sprint.html', {'backlog': backlog})


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
