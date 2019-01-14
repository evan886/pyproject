from django.db import models
from dbmodel.base_model import BaseModel
from utils.encryption import Encrytion


class UserAccountManager(models.Manager):
    '''账户类模型管理器'''
    def addUser(self,username,password,email):
        className = self.model
        # sha1加密密码后存入数据库
        password = Encrytion.sha1(password)
        obj = className(username=username,password=password,email=email)
        obj.save()
        return obj

    def findUserByName(self,username):
        className = self.model
        objs = className.objects.filter(username=username)
        if objs is None or len(objs) == 0:
            return False
        else:
            return True

    def findUserByName_pwd(self,username,pwd):
        className = self.model
        pwd = Encrytion.sha1(pwd)
        obj = className.objects.filter(username=username,password=pwd)
        if obj is None or len(obj) == 0:
            return None
        else:
            # 查询结果是集合,应返回一个用户
            return obj[0]


class UserAccount(BaseModel):
    '''账户类模型'''
    username = models.CharField(max_length=20,verbose_name='用户名')
    password = models.CharField(max_length=40,verbose_name='密码')
    email = models.EmailField(verbose_name='用户邮箱')

    objects = UserAccountManager()  # 管理器类

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_account'



class AddressManager(models.Manager):
    '''地址类模型管理器'''

    # 查询数据库是否有该用户地址信息(没有就将添加的地址设置为默认地址)
    def query_user_addr(self, uid, is_default=False):
        rets = self.filter(passport__id=uid, is_default = is_default)
        return rets


    # 添加对象进数据库
    def add_address(self, name, addr , code, phone, uid):
        is_default = False
        rets = self.query_user_addr(uid,is_default=True)
        if len(rets) == 0:
            is_default = True
        model_class = self.model
        # 创建对象
        obj = model_class(passport_id = uid,recipient_name = name,recipient_addr = addr,
        recipient_phone = phone,zip_code = code,is_default = is_default)
        obj.save()
        return obj

    # 修改默认地址
    def modify_default_addr(self, user_id, addr_id):
        default_addr = self.query_user_addr(user_id, is_default=True)[0]
        default_addr.is_default = False
        new_addr = self.filter(id=addr_id)[0]
        new_addr.is_default = True
        new_addr.save()
        default_addr.save()




class Address(BaseModel):
    '''地址类模型'''
    passport = models.ForeignKey('UserAccount', verbose_name = '所属账户')
    recipient_name = models.CharField(max_length = 24, verbose_name = '收件人')
    recipient_addr = models.CharField(max_length = 256, verbose_name = '收件人地址')
    recipient_phone = models.CharField(max_length = 11, verbose_name = '收件人电话')
    zip_code = models.CharField(max_length = 6, verbose_name = '邮政编号')
    is_default = models.BooleanField(default = False, verbose_name = '是否是默认收件地址')

    objects = AddressManager()

    def __str__(self):
        return {'passport':self.passport,'name':self.recipient_name,'addr':self.recipient_addr,
        'phone':self.recipient_phone,'code':self.zip_code,'is_default':self.is_default}

    class Meta:
        db_table = 'user_address'














# 模块测试代码
if __name__ == '__main__':
    res = UserAccount.objects.findUserByName_pwd('python','asdfasdf')
    print(res)
