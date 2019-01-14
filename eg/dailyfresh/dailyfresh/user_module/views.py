from django.shortcuts import render,redirect
from .models import UserAccount,Address
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from . import tasks

def register(res):
    return render(res,'user_module/register.html')

def register_handler(res):
    args = res.POST
    username = args.get('user_name')
    password = args.get('pwd')
    email = args.get('email')

    obj = UserAccount.objects.addUser(username,password,email)
    # message = '<h1>欢迎你成为天天生鲜会员</h1>请牢记用户名和密码</br> username:'+username
    # send_mail('天天生鲜网','',settings.EMAIL_FROM,[email],html_message=message)

    # celery 发送邮件
    tasks.sendmail.delay(username,email)

    # return HttpResponse('register ok name:'+obj.username)
    return render(res,'user_module/login.html')

# 登录页面
def login(res):
    # 判断用户是否选择过记住用户名
    name = None
    if 'username' in res.COOKIES:
        name = res.COOKIES.get('username')
    else:
        name = ''

    return render(res, 'user_module/login.html',{'default_name':name})


# 处理前端的ajax提交的 验证用户名是否重复的函数
def check_name(res):
    name = res.GET.get('username')
    res = UserAccount.objects.findUserByName(name)
    if not res:
        # 找到此昵称用户
        return JsonResponse({'res':1 })
    else:
        return JsonResponse({'res':0 })


# 处理前端的ajax提交的 登录验证函数
def check_login_status(res):
    print('in check')
    # name = res.GET.get('username')
    # pwd = res.GET.get('password')
    name = res.POST.get('username')
    pwd = res.POST.get('password')
    rember = res.POST.get('rember')
    user = UserAccount.objects.findUserByName_pwd(name, pwd)
    if user is not None:
        jres = JsonResponse({'res':1})
        # 给cookie 赋值,记住用户名
        if rember:
            addcookie(jres, 'username', name)
        return jres
    else:
        return JsonResponse({'res': 0})


# 处理登录请求的函数
def login_handler(res):
    args = res.POST
    username = args.get('username')
    password = args.get('pwd')
    remberstatus = args.get('remberaccount')
    user = UserAccount.objects.findUserByName_pwd(username,password)

    # 给session 赋值,记录用户状态
    res.session['loginstatus'] = 1
    res.session['username'] = username
    res.session['userid'] = user.id

    # 默认登录后的访问页面为首页
    next_url = '/user/index/'
    # 判断用户在登录之前是否有预定地址
    if res.session.has_key('pre_url'):
        next_url = res.session['pre_url']

    return redirect(next_url)

# 首页地址
def index(res):
    return render(res, 'user_module/index.html')

# 添加cookie 默认添加cookie的失效时间是30天
def addcookie(response,key,val):
    response.set_cookie(key,val,max_age=30*24*60*60)

# 获取登录状态
def login_status(res):
    status = res.session.get('loginstatus',0)
    print('status = %s' % status)
    return JsonResponse({'res':status})

# 退出登录
def quit_login(res):
    del res.session['loginstatus']
    # res.session.clear()
    return JsonResponse({'res':1})

# 获取用户信息页面
def user_center_info(res):
    param = {'page':'user'}
    user_id = res.session.get('userid')
    default_addr = Address.objects.query_user_addr(user_id,is_default=True)
    if len(default_addr) == 1:
        param['default_addr'] = default_addr[0]
    return render(res, 'user_module/user_center_info.html', param)

# 获取用户订单页面
def user_center_order(res):
    param = {'page':'order'}
    return render(res, 'user_module/user_center_order.html', param)

# 获取用户收货地址页面
def user_center_address(res):
    param = {'page':'addr'}
    user_id = res.session.get('userid')
    # 查询默认地址
    default_addr = Address.objects.query_user_addr(user_id,is_default=True)
    if len(default_addr) == 1:
        param['default_addr'] = default_addr[0]

    # 查询所有非默认地址
    addrs = Address.objects.query_user_addr(user_id)
    param['addrs'] = addrs
    return render(res, 'user_module/user_center_site.html', param)


# 添加收货地址
def add_address(res):
    args = res.POST
    name = args.get('recipient_name')
    address = args.get('recipient_addr')
    zip_code = args.get('zip_code')
    tel = args.get('recipient_phone')
    user_id = res.session.get('userid')

    obj = Address.objects.add_address(name,address,zip_code,tel,user_id)
    return redirect('/user/')


# 修改默认收货地址
def change_default_addr(res):
    print('in change_default_addr')
    index = res.GET.get('index')
    user_id = res.session.get('userid')
    addrs = Address.objects.query_user_addr(user_id)
    addr_id = addrs[int(index)].id
    Address.objects.modify_default_addr(user_id, addr_id)
    return JsonResponse({'res':1})



















def endfile():
    pass
