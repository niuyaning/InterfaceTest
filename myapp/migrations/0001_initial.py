# Generated by Django 2.2.1 on 2019-05-08 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='项目描述')),
                ('LastUpdateTime', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('createTime', models.DateTimeField(auto_now=True, max_length=1000, null=True, verbose_name='创建时间')),
                ('member', models.CharField(blank=True, max_length=520, null=True, verbose_name='项目成员')),
                ('owner', models.ForeignKey(max_length=1000, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'ordering': ['-createTime'],
            },
        ),
        migrations.CreateModel(
            name='HttpApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='接口名称')),
                ('requestType', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=50, verbose_name='请求方式')),
                ('apiurl', models.CharField(max_length=1024, verbose_name='接口地址')),
                ('requestParameterType', models.CharField(blank=True, choices=[('form-data', '表单(form-data)'), ('raw', '原数据(raw)')], max_length=50, null=True, verbose_name='请求参数格式')),
                ('requestHeader', models.TextField(blank=True, max_length=2048, null=True, verbose_name='请求header')),
                ('requestBody', models.TextField(blank=True, max_length=2048, null=True, verbose_name='请求体')),
                ('lastUpdateTime', models.DateTimeField(auto_now=True, verbose_name='最近更新时间')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('assertType', models.CharField(choices=[('noselect', '无'), ('in', '包含'), ('status_code', '状态码')], default='', max_length=200, verbose_name='断言类型')),
                ('assertContent', models.CharField(default='', max_length=200, verbose_name='断言内容')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Project', verbose_name='所属项目')),
                ('userUpdate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
        ),
    ]
