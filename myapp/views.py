from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Project,HttpApi
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request,'index.html')
'''
登录
'''
def user_login(request):
    if request.method=="GET":
        return render(request, "login.html")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
           login(request,user)
           return redirect("project_list")
        else:
           msg="用户名或密码错误"
           return render(request,"login.html",{"msg":msg})
'''
退出
'''
@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")
'''
项目列表
'''
class ProjectListView(LoginRequiredMixin,generic.ListView):
    model=Project
    template_name = 'project/project_list.html'
    paginate_by=5
'''
新建项目
'''
@login_required
def project_create(request):
    if request.method=="GET":
        return render(request,"project/project_create.html")
    if request.method=="POST":
        project_name=request.POST.get("project_name")
        #strip 去除首尾空格
        project_description=request.POST.get("project_description").strip()
        project_owner_str=request.POST.get("project_owner").strip()
        try:
            project_owner=User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg="指定的项目负责人 %s 不存在" % project_owner_str
            return render(request,"project/project_create.html",{"errmsg":errmsg})
        project_member_str=request.POST.get("project_member").strip();
        if project_member_str:
            member_list=project_member_str.strip().split("\n")
            for member in member_list:
                username=member.strip()
                try:
                    User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg="指定的项目成员 %s 不存在"%username
                    return render(request,"project/project_create.html",{"errmsg":errmsg})
            project_member=",".join(member_list)
        else:
            project_member=""
        project=Project(name=project_name,description=project_description,owner=project_owner,member=project_member)
        project.save();
        return redirect("project_detail",project.id)
'''
项目编辑页面
'''
@login_required
def  project_edit(request,pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        if project.member is None:
            project.member = ""
        else:
            project.member = project.member.replace(",", "\n")
        return render(request, "project/project_create.html", {"project": project})
    if request.method == "POST":
        project = Project.objects.get(id=pk)
        project.name = request.POST.get("project_name")
        project_owner_str = request.POST.get("project_owner")
        try:
            project.owner = User.objects.get(username=project_owner_str.strip())
        except ObjectDoesNotExist:
            errmsg = "指定的项目负责人不存在"
            if project.member is None:
                project.member = ""
            return render(request, "project/project_create.html", {"project": project, "errmsg": errmsg})
        project.description = request.POST.get("project_description").strip()
        project_member_str = request.POST.get("project_member").strip()

        if project_member_str:
            member_list = project_member_str.strip().split("\n")
            for item in member_list:
                username = item.strip()
                try:
                    User.objects.get(username=username)
                except ObjectDoesNotExist:
                    errmsg = "项目成员%s不存在" % username
                    return render(request, "project/project_create.html", {"project": project, "errmsg": errmsg})
            project.member = ','.join(member_list)
        else:
            project.member = ""
        project.save()
        return redirect("project_detail", project.id)

'''
项目详情页
'''
class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
    model = Project
    template_name = "project/project_detail.html"
'''
删除项目
'''
@csrf_exempt
def project_delete(request,pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        print(project.id)
        return render(request, "project/project_delete.html", {"project": project})
    if request.method == "POST":
        project = Project.objects.get(id=pk)
        project.delete()
        return HttpResponse("删除数据成功")
        return redirect("project_list",project.id)
'''
项目搜索
'''
def project_search(request):
    q=request.GET.get('q')
    print(q)
    errmsg = ''
    if q is None:
        errmsg="请输入项目名称"
        return render(request,'project/project_search.html',{"errmsg":errmsg})
    project = Project.objects.filter(name__contains=q)
    print(project)
    return render(request,'project/project_search.html',{"project": project, "errmsg": errmsg})

'''
接口列表
'''
@login_required
def interface_list(request,pk):
    project=Project.objects.get(id=pk)
    rs=HttpApi.objects.filter(project=project).order_by("-lastUpdateTime")
    paginator=Paginator(rs,5)
    page=request.GET.get("page")
    httpapis=paginator.get_page(page)
    return render(request,"project/interface_list.html",{"project":project,"objects":httpapis})

'''
新建接口
'''
@login_required  #跳过登录
def interface_create(request,pk):
    if request.method=="GET":
        project=Project.objects.get(id=pk)
        return render(request,"project/interface_create.html",{"project":project})
    if request.method=="POST":
        httpapi_project=Project.objects.get(id=pk)
        httpapi_name=request.POST.get("httpapi_name")
        httpapi_description=request.POST.get("httpapi_description")
        httpapi_url=request.POST.get("httpapi_url")
        httpapi_requesttype=request.POST.get("httpapi_requesttype")
        httpapi_requestheader=request.POST.get("httpapi_requestheader")
        httpapi_requestparametertype=request.POST.get("httpapi_requestparametertype")
        httpapi_requestbody=request.POST.get("httpapi_requestbody")
        httpapi_asserttype=request.POST.get("httpapi_asserttype")
        httpapi_assertcontent=request.POST.get("httpapi_assertcontent")
        userupdate=request.user
        httpapi=HttpApi(
            project=httpapi_project,
            name=httpapi_name,
            requestType=httpapi_requesttype,
            apiurl=httpapi_url,
            requestParameterType=httpapi_requestparametertype,
            requestHeader=httpapi_requestheader,
            requestBody=httpapi_requestbody,
            userUpdate=userupdate,
            description=httpapi_description,
            assertType=httpapi_asserttype,
            assertContent=httpapi_assertcontent,
        )
        httpapi.save()
        return redirect("interface_list",httpapi_project.id)
'''
接口编辑
'''
@login_required
def interface_edit(request,project_id,httpapi_id):
    if request.method=="GET":
        project=Project.objects.get(id=project_id)
        httpapi=HttpApi.objects.get(project=project,id=httpapi_id)
        return render(request,"project/interface_create.html",{"project":project,"object":httpapi})
    if request.method=="POST":
        project=Project.objects.get(id=project_id)
        httpapi=HttpApi.objects.get(project=project,id=httpapi_id)
        httpapi.name=request.POST.get("httpapi_name")
        httpapi.description=request.POST.get("httpapi_description")
        httpapi.httpapi_url=request.POST.get("httpapi_url")
        httpapi.httpapi_requesttype=request.POST.get("httpapi_requesttype")
        httpapi.httpapi_requestheader=request.POST.get("httpapi_requestheader")
        httpapi.httpapi_requestparametertype=request.POST.get("httpapi_requestparametertype")
        httpapi.httpapi_requestbody=request.POST.get("httpapi_requestbody")
        httpapi.httpapi_asserttype=request.POST.get("httpapi_asserttype")
        httpapi.httpapi_assertcontent=request.POST.get("httpapi_assertcontent")
        httpapi.userUpdate=request.user
        httpapi.save()
        return redirect("interface_list",project.id)









