from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):

    def _init_(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('User:login'))
        else:
            print('asda')

    # def process_view(self, request, view_func, *view_args, **view_kargs):
    #     print(request.path)
    #     print(view_func.__name__)
    #     print(view_args)
    #     print(view_kargs)
    #     if not request.user.is_authenticated:
    #         print('ee')
    #         # return HttpResponseRedirect(reverse('User:login'))

        # if request.user.is_staff():
        #     print('badimcan')
        # return None

