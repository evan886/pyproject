import django.middleware


class RecordUrl(object):

    exclude_url = ['/user/login','/user/quitlogin','/user/register']

    def process_view(self, request, view_func, *args, **kwargs):
        if request.path not in RecordUrl.exclude_url and not request.is_ajax():
            request.session['pre_url'] = request.path