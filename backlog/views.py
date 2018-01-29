from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url
from .models import BackLog, Sprint
from .forms import LoginForm, RegisterForm, NewSprint

User = get_user_model()


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


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'