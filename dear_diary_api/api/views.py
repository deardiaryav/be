from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import MasterTable,userLogin,Session
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect,render
from django.contrib.auth.hashers import check_password
from main.models import userLogin
from .serializers import userLoginSerializer,MasterTableSerializer 
from rest_framework import status
from uuid import uuid4
from django.utils import timezone

@api_view(['Get'])
def api(request):
    ls_api={
        'Home':'',
        'Register':'register/',
        'userExist':'checkuser/',
        'userAuthantication':'user/auth/',
        'api':'api/',
        'renamePage':'renamePage/',
        'creating pageData':'home/userid/page/createpagedata/',
        'Updating pageData':'home/userid/page/updatepagedata/',
        'Showing pageData':'home/userid/page/',

        }
    return Response(ls_api)

'''@api_view(['POST'])
def login(request):
    data=request.data
    session_key=data.get('session_key')
    userid=data.get('userid')
    user=userLogin.objects.get(userid=userid)
    try:
        session=Session.objects.get(session_key=session_key)
        if session.user==user:
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    except Session.DoesNotExist:
        #pass
        pswd=data.get('pswd')
        try:
            user=userLogin.objects.get(userid=userid)
            print(user)
            if not(check_password(pswd,user.pswd)):
                session1=Session.create(user, session_key)
                return HttpResponse(True)
            else:
                return HttpResponse(False)
        except userLogin.DoesNotExist:
            return HttpResponse(False)'''
@api_view(['POST'])
def login(request):
    data=request.data
    userid=data.get('userid')
    pswd=data.get('pswd')
    user=userLogin.objects.get(userid=userid, pswd=pswd)
    session=Session.objects.filter(user=user)
    if session.exists():
        session=session.first()
        return HttpResponse(session.session_key)
    else:
        session_key=uuid4()
        session=Session.objects.create(user=user,session_key=session_key)
        return HttpResponse(session.session_key)
    
@api_view(['GET','POST'])
def checkLogin(request):
    data=request.query_params
    session_key=data['session_key']
    session=Session.objects.filter(session_key=session_key)
    if session.exists() and ((timezone.now()-session.first().last_activity).total_seconds()>3600):
        session.first().delete()
        return HttpResponse(False)
    return HttpResponse(session.exists())

 
@api_view(['POST'])
def logout(request):
    data=request.data
    session_key=data['session_key']
    session=Session.objects.get(session_key=session_key)
    session.delete()
    return HttpResponse(True)

@api_view(['GET'])
def home(request, userid):
    table=MasterTable.objects.all()
    user=table.filter(userid=userid)
    sections=[userid]
    pages=[]
    for section in sections:
        page=user.filter(userid=userid)
        section_page=[]
        for j in page:
            section_page.append(j.page)
        pages.append(section_page)
    data=dict(zip(sections, pages))
    return Response(data)

@api_view(['POST'])
def addUser(request):
    serializer=userLoginSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse("True")
    return HttpResponse("False")

@api_view(['GET'])
def userExist(request,userid):
    user=userLogin.objects.all()
    for i in user:
         if str(userid)==str(i.userid):
            return HttpResponse("True")
        
    return HttpResponse("False")

@api_view(['POST'])
def userAuth(request):
    user=userLogin.objects.all()
    inUser=request.data
    for i in user:
        if ((str(i.userid)==str(inUser['userid'])) & (str(i.pswd) == str(inUser['pswd']))):
            return HttpResponse("True")
    return HttpResponse("False")

@api_view(['GET'])
def landing(request):
    return HttpResponse('<h1>Home Page</h1>')

@api_view(['GET'])
def pagedata(request,userid,page):
    table=MasterTable.objects.all()
    pageData=table.filter(userid=userid,page=page)
    serializer= MasterTableSerializer(pageData,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def pagedatacreate(request,userid,page):
    dataReceived = request.data
    user=userLogin.objects.all().filter(userid=userid).first()
    dataReceived['userid']=user.userid
    serializer = MasterTableSerializer(data=dataReceived)
    if MasterTable.objects.filter(**dataReceived).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif serializer.is_valid():
        serializer.save()
    return Response(dataReceived)


@api_view(['PUT'])
def pagedataupdate(request,userid,page):
    dataReceived = request.data
    user=userLogin.objects.all().filter(userid=userid).first()
    dataReceived['userid']=user.userid
    table=MasterTable.objects.get(userid=userid,page=page)
    serializer=MasterTableSerializer(instance=table, data=request.data)
    if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return HttpResponse("True")
        
@api_view(['POST'])
def renamePage(request):
    userid=request.GET.get('userid')
    page=request.GET.get('page')
    new_page=request.GET.get('new_page')
    t=MasterTable.objects.get(userid=userid,page=page)
    t.page=new_page
    t.save()
    return redirect('/home/%s' %userid)

@api_view(['GET','DELETE'])
def deletePage(request,userid,page):
    # data=request.query_params
    # dataReceived = request.data
    # user=userLogin.objects.all().filter(userid=userid).first()
    # userid=data['userid']
    # page=data['page']
    t=MasterTable.objects.get(userid=userid,page=page)
    print(t.userid)
    t.delete()
    return redirect('/home/%s' %userid)
    # data=request.data
    # userid=data['userid']
    # user=userLogin.objects.all().filter(userid=userid).first()
    # data['userid']=user.userid
    # userid=data['userid']
    # page=data['page']
    # t=MasterTable.objects.get(userid=userid,page=page)
    # t.delete()
    # return redirect('/home/%s' %userid)

@api_view(['GET'])
def pagewithdata(request, userid):
    table=MasterTable.objects.all()
    user=table.filter(userid=userid)
    pages=[]
    datas=[]
    x=[]
    for i in user:
        pages.append(i.page)
    pages=[*set(pages)]
    for page in pages:
        data=user.filter(page=page)
        for j in data:
            datas.append(j.data)
    data1=dict(zip(pages, datas))
    a=[]
    for k in data1.items():
        a.append({"page":k[0],"data":k[1]})
    return Response(a)

