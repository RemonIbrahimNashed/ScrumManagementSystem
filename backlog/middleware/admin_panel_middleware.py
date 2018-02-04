from django.urls import reverse
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class RestrictAdminPageMiddleware(MiddlewareMixin):
    # A middleware that restricts staff members access to administration panels.

    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated:
                if not (request.user.is_admin()):
                    raise Http404("You are not Authorized to enter this page")
            else:
                raise Http404("You are not Authorized to enter this page")