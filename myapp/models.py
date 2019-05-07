from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):

    '''
    项目信息
    '''

    #项目名称
    name=models.CharField(max_length=50,verbose_name='项目名称')
    #项目描述
    description=models.CharField(max_length=1000,blank=True,null=True,verbose_name='项目描述')
    #最近修改时间
    LastUpdateTime=models.DateTimeField(auto_now=True,verbose_name='最近修改时间')
    #创建时间
    createTime=models.DateTimeField(auto_now=models.SET_NULL,null=True,max_length=1000,verbose_name="创建时间")
    #创建人
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,max_length=1000,verbose_name='创建人')
    #项目成员
    member=models.CharField(max_length=520,blank=True,null=True,verbose_name='项目成员')

    def __str__(self):
        return self.name
    class Meta:
        ordering=["-createTime"]

'''
定义接口请求方式 post/get/put/delete
'''
REQUEST_TYPE_CHOICE=(
    ('POST','POST'),
    ('GET','GET'),
    ('PUT','PUT'),
    ('DELETE','DELETE')
)
'''
定义请求参数格式
'''
REQUEST_PARAMETER_TYPE_CHOICE=(
    ('form-data','表单(form-data)'),
    ('raw','原数据(raw)')
)
'''
定义断言类型
'''
ASSERT_TYPE=(
    ('noselect','无'),
    ('in','包含'),
    ('status_code','状态码')
)
class HttpApi(models.Model):
    '''
    接口信息
    '''
    #所属项目
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name="所属项目")
    #接口名称
    name=models.CharField(max_length=50,verbose_name="接口名称")
    #请求方式
    requestType=models.CharField(max_length=50,verbose_name="请求方式",choices=REQUEST_TYPE_CHOICE)
    #接口地址
    apiurl=models.CharField(max_length=1024,verbose_name="接口地址")
    #请求参数格式
    requestParameterType=models.CharField(max_length=50,verbose_name="请求参数格式",blank=True,null=True,choices=REQUEST_PARAMETER_TYPE_CHOICE)
    #请求头
    requestHeader=models.TextField(max_length=2048,verbose_name="请求header",blank=True,null=True)
    #请求体
    requestBody=models.TextField(max_length=2048,verbose_name="请求体",blank=True,null=True)
    #最近更新时间
    lastUpdateTime=models.DateTimeField(auto_now=True,verbose_name="最近更新时间")
    #更新人
    userUpdate=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name="更新人")
    #描述
    description=models.CharField(max_length=1024,blank=True,null=True,verbose_name="描述")
    #断言类型
    assertType=models.CharField(max_length=200,verbose_name="断言类型",default="",choices=ASSERT_TYPE)
    #断言内容
    assertContent=models.CharField(max_length=200,verbose_name="断言内容",default="")

    def __str__(self):
        return self.name





