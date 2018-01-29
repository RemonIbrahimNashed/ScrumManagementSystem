from django.conf.urls import url
from django.contrib import admin
from backlog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^backlogs/(?P<pk>\d+)/$', views.backlog_sprints, name='backlog_sprints'),
    url(r'^backlogs/(?P<pk>\d+)/new/$', views.new_sprint, name='new_sprint'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),

]
