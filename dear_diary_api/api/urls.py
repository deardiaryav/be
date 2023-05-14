from django.urls import path
from . import views

urlpatterns=[
    path('',views.landing),
    path('api/',views.api),
    path('renamepage/', views.renamePage),
    path('register/',views.addUser),
    path("user/auth/",views.userAuth),
    path('renamePage/', views.renamePage),
    path('deletePage/<str:userid>/<str:page>', views.deletePage),
    path('home/<str:userid>/', views.home, name='home'),
    path('home/<str:userid>/<str:page>/',views.pagedata),
    #url for creating a new pagedata
    path('home/<str:userid>/<str:page>/createpagedata/',views.pagedatacreate),
    #url for updating a already existing pagadata
    path('home/<str:userid>/<str:page>/updatepagedata/',views.pagedataupdate),
    path('login/', views.login),
    path('logout/', views.logout),
    path('checkLogin/', views.checkLogin),
    path("<str:userid>/",views.userExist),
    path("pagewithdata/<str:userid>/",views.pagewithdata)
]
