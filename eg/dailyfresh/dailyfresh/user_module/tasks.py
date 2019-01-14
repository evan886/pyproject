import time
from celery import task
from django.conf import settings
from django.core.mail import send_mail

@task
def sendmail(username,email):
    message = '<h1>欢迎你成为天天生鲜会员</h1>请牢记用户名和密码</br> username:' + username
    send_mail('天天生鲜网', '', settings.EMAIL_FROM, [email], html_message=message)