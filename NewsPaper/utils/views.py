from django.shortcuts import redirect
from django.views import View


class TimeZone(View):
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META.get('HTTP_REFERER'))
