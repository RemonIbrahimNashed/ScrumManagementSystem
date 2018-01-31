from django.conf.urls import url
from django.contrib import admin
from backlog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home, name='home'),
    url(r'^backlogs/new/$', views.new_backlog, name='new_backlog'),
    url(r'^backlogs/(?P<pk>\d+)/$', views.backlog_sprints, name='backlog_sprints'),
    url(r'^backlogs/(?P<pk>\d+)/sprints/(?P<spk>\d+)/$', views.sprint_tasks, name='sprint_tasks'),
    url(r'^backlogs/(?P<pk>\d+)/sprints/(?P<spk>\d+)/new$', views.new_task, name='new_task'),
    url(r'^backlogs/(?P<pk>\d+)/new/$', views.new_sprint, name='new_sprint'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^$', views.LoginView.as_view(), name='login'),



]
