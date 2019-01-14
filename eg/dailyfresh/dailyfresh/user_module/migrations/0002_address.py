# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='标记位')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('recipient_name', models.CharField(max_length=24, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='收件人地址')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='收件人电话')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮政编号')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否是默认收件地址')),
                ('passport', models.ForeignKey(to='user_module.UserAccount', verbose_name='所属账户')),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]
