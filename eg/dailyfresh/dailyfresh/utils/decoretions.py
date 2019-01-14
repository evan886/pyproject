from django.shortcuts import redirect

def login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.session.has_key('loginstatus'):
            # 已登录
            return func(request,*args,**kwargs)
        else:
            return redirect('/user/login/')
    return wrapper