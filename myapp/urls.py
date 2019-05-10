from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    #登录
    path('login/',views.user_login,name='user_login'),
    #退出
    path('logout/',views.user_logout,name='user_logout'),
    #项目列表
    path('project/', views.ProjectListView.as_view(), name='project_list'),
    #新建项目
    path('project/create',views.project_create,name='project_create'),
    #项目详情
    path('project/<int:pk>',views.ProjectDetailView.as_view(),name='project_detail'),
    #编辑项目
    path('project/<int:pk>/edit',views.project_edit,name='project_edit'),
    #删除项目
    path('project/<int:pk>/delete',views.project_delete,name='project_delete'),
    #搜索项目
    path('project/search',views.project_search,name='project_search'),
    #接口列表
    path('project/<int:pk>/interface/list',views.interface_list,name='interface_list'),
    #新建接口
    path('project/<int:pk>/interface/create',views.interface_create,name='interface_create'),
    #编辑接口
    path('project/<int:project_id>/httpapi/<int:httpapi_id>/edit',views.interface_edit,name="interface_edit")
 ]

