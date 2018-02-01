from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import get_user_model
from django.utils.http import is_safe_url
from .forms import NewSprint, NewBackLog, NewTask, LoginForm, RegisterForm, TaskModificationForm
from django.contrib.auth.decorators import login_required
from django import template
from .models import UserManager

register = template.Library()

User = get_user_model()


@register.filter()
def lookup(d, key):
    return d[key]


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "/"

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
                return redirect_path
        return self.default_next


# Create your views here.
from .models import BackLog, Sprint, Task


@login_required
def home(request):
    backlogs = BackLog.objects.all()
    li = []
    for backlog in backlogs:
        counter = 0
        for sprint in backlog.sprints.all():
            counter += sprint.tasks.all().count()
        li.append(counter)
    return render(request, 'home.html', {'backlogs': backlogs, 'li': li})



@login_required
def backlog_sprints(request, pk):
    backlog = get_object_or_404(BackLog, pk=pk)
    return render(request, 'sprint.html', {'backlog': backlog})


@login_required
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


@login_required
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
            assigned_user=None

        )
        return redirect('sprint_tasks', pk, spk)
    return render(request, 'new_task.html', {'backlog': backlog, 'sprint': sprint, 'form': NewTask})


@login_required
def new_backlog(request):
    if request.method == 'POST':
        backlog = BackLog.objects.create(
            name=request.POST['name'],
            end_at=request.POST['dead_line'],
        )
        return redirect('home')
    return render(request, 'new_backlog.html', {'form': NewBackLog})


@login_required
def sprint_tasks(request, pk, spk):
    backlog = get_object_or_404(BackLog, pk=pk)
    sprint = get_object_or_404(Sprint, pk=spk)
    if request.method == 'POST':
        try:
            selected_task = sprint.tasks.get(pk=request.POST['task'])
            if selected_task.status == 2 and selected_task.assigned_user == request.user and request.user.is_admin:
                selected_task.status = 3
            elif selected_task.status == 2 and not request.user.is_admin:
                selected_task.status = 3
            elif not selected_task.assigned_user:
                selected_task.assigned_user = request.user
                selected_task.status = 2
            else:
                selected_task.assigned_user = None
                selected_task.status = 1
            selected_task.save()
        except (KeyError, Task.DoesNotExist):
            print("Not Selected")
        return render(request, "task.html", {'backlog': backlog, 'sprint': sprint, 'request': request})

    if request.method == 'GET':
        return render(request, 'task.html', {'backlog': backlog, 'sprint': sprint, 'request': request})


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/home'
    template_name = 'login.html'
    default_next = '/home'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'


def modify_task(request, pk, spk):
    backlog = get_object_or_404(BackLog, pk=pk)
    sprint = get_object_or_404(Sprint, pk=spk)
    selected_task = sprint.tasks.get(pk=request.GET['task'])

    if request.method == 'POST' and request.user.is_admin:
        form = TaskModificationForm(request.POST)
        if form.is_valid():
            object = UserManager()
            selected_task.name          = request.POST['name']
            selected_task.description   = request.POST['description']
            selected_task.end_at        = request.POST['dead_line']
            selected_task.importance    = request.POST['importance']
            selected_task.assigned_user = User.object.all().get(email=form.cleaned_data['assigned_user'])
            selected_task.save()
            return redirect('sprint_tasks', pk, spk)
    return render(request, 'modify.html', {'task': selected_task, 'sprint': sprint, 'form': TaskModificationForm})
