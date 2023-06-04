from pdb import post_mortem
from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .serializers import ServerUserSerializer,ServerBanSerializer,UserCountDateSerializer,UserCountWeekSerializer,UserSentenceSerializer,ServerSlangSerializer
from django.core import serializers
from django.urls import reverse
from . import models
from datetime import datetime,date
import json
# Create your views here.

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def check_sentence(request,serverid,userid):
    sentence_info = list(models.user_sentence.objects.filter(server=serverid,user=userid).values())
    return JsonResponse({"user": sentence_info[1],"server":sentence_info[0],"sentence":sentence_info[3]}, safe=False, status=status.HTTP_200_OK)

def store_slang(request):
    if request.method == 'POST':
        slang=models.slang_dict()
        slang.slang_text=request.POST['slang']
        slang.save()
        return redirect('home')

    else:
        return render(request, 'add_slang.html')
      
        

@csrf_exempt
def store_sentence(request):
    requestedData = JSONParser().parse(request)
    print(requestedData)
    serverid=requestedData["server"]
    userid=requestedData["user"]
    sentence_str=requestedData["sentence"]
    time=datetime.now()
    date=datetime.today()
    year=time.isocalendar()[0]
    week=time.isocalendar()[1]
    count=0

    UserSentence=models.user_sentence()
    UserSentence.user=userid
    UserSentence.server=serverid
    UserSentence.sentence=sentence_str
    UserSentence.datetime=time
    UserSentence.save()
    print(sentence_str)
    slang=models.slang_dict.objects.all()
    ban=models.server_banned.objects.filter(server=serverid)
        
    for s in slang:
        if sentence_str.count(s.slang_text)>0:
            count=count+sentence_str.count(s.slang_text)
    for b in ban:
        if sentence_str.count(b.banned)>0:
            count=count+sentence_str.count(b.banned)
    print(count)
    
    user_count_date_check=models.user_slang_count_date.objects.filter(server=serverid,user=userid,date=date).exists()
    if user_count_date_check == False:
        user_count_date=models.user_slang_count_date()
        user_count_date.user=userid
        user_count_date.server=serverid
        user_count_date.date=date
        user_count_date.count=count
        
        user_count_date.save()

    else:
        user_count_date=models.user_slang_count_date.objects.get(server=serverid,user=userid,date=date)
        user_count_date.count=user_count_date.count+count
        user_count_date.id=user_count_date.id

        user_count_date.save()

    user_count_week_check=models.user_slang_count_week.objects.filter(server=serverid,user=userid,year=year,week=week).exists()
    if user_count_week_check == False:
        user_count_week=models.user_slang_count_week()
        user_count_week.user=userid
        user_count_week.server=serverid
        user_count_week.year=year
        user_count_week.week=week
        user_count_week.count=count

        user_count_week.save()        
    else:
        user_count_week=models.user_slang_count_week.objects.get(server=serverid,user=userid,year=year,week=week)
        user_count_week.count=user_count_week.count+count
        user_count_week.id=user_count_week.id

        user_count_week.save()        

    return JsonResponse({"user": userid,"server":serverid,"count":count}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def store_user(request):
    requestedData = JSONParser().parse(request)
    serializers = ServerUserSerializer(data=requestedData)
    if models.server_user.objects.filter(server=requestedData['server'],user=requestedData['user']).exists():
        return JsonResponse({"MESSAGE": "The user "+requestedData['user']+" is already exists in server"+requestedData['server']},safe=False,status=status.HTTP_400_BAD_REQUEST)
    
    elif serializers.is_valid():
        serializers.save()
        return JsonResponse({"MESSAGE": "Success to Add"},safe=False, status=status.HTTP_201_CREATED)

@csrf_exempt
def store_count_date(request):
    requestedData = JSONParser().parse(request)
    serializers = UserCountDateSerializer(data=requestedData)
    count=int(requestedData['count'])
    serverid=requestedData['server']
    userid=requestedData['user']
    dateid=requestedData['date']
    if models.user_slang_count_date.objects.filter(server=serverid,user=userid,date=dateid).exists():
        storecount=models.user_slang_count_date.objects.get(server=serverid,user=userid,date=dateid)
        storecount.count=storecount.count+count
        storecount.id=storecount.id

        storecount.save()
    elif serializers.is_valid():
        serializers.save()
    
    return JsonResponse({"MESSAGE": "Success to Add"},safe=False, status=status.HTTP_201_CREATED)



@csrf_exempt
def store_count_week(request):

    requestedData = JSONParser().parse(request)
    serializers = UserCountDateSerializer(data=requestedData)
    count=int(requestedData['count'])
    serverid=requestedData['server']
    userid=requestedData['user']
    yearid=requestedData['year']
    weekid=requestedData['week']
    if models.user_slang_count_week.objects.filter(server=serverid,user=userid,year=yearid,week=weekid).exists():
        storecount=models.user_slang_count_week.objects.get(server=serverid,user=userid,year=yearid,week=weekid)
        storecount.count=storecount.count+count
        storecount.id=storecount.id

        storecount.save()
    elif serializers.is_valid():
        serializers.save()
    
    return JsonResponse({"MESSAGE": "Success to Add"},safe=False, status=status.HTTP_201_CREATED)


@csrf_exempt
def user_count_week(request,serverid,userid,year,week):
    user_count_week_info = models.user_slang_count_week.objects.get(server=serverid,user=userid,year=year,week=week)
    user_count_date_json={"user":user_count_week_info.user,"server":user_count_week_info.server,"count":user_count_week_info.count,"year":user_count_week_info.year,"week":user_count_week_info.week}

    return JsonResponse(user_count_date_json, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def user_count_date(request,serverid,userid,year,month,day):
    dateid=date(year,month,day)

    user_count_date_info = models.user_slang_count_date.objects.get(server=serverid,user=userid,date=dateid)
    user_count_date_json={"user":user_count_date_info.user,"server":user_count_date_info.server,"count":user_count_date_info.count,"date":dateid}
    print(user_count_date_json,type(user_count_date_json))
    return JsonResponse(user_count_date_json, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def server_count_week(request,serverid,year,week):
    server_count_week_info = list(models.user_slang_count_week.objects.filter(server=serverid,year=year,week=week).order_by('-user').values())
    result=[]
    for server_count in server_count_week_info:
        result.append(server_count)
    print(result,type(result))
    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def server_count_date(request,serverid,year,month,day):
    dateid=date(year,month,day)
    server_count_date_info = list(models.user_slang_count_date.objects.filter(server=serverid,date=dateid).order_by('-user').values())
    result=[]
    for server_count in server_count_date_info:
        result.append(server_count)

    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def store_ban(request):
    requestedData = JSONParser().parse(request)
    serializers = ServerBanSerializer(data=requestedData)
    serverid=requestedData['server']
    banned=requestedData['banned']
    if models.server_banned.objects.filter(server=serverid,banned=banned).exists():
        return JsonResponse({"MESSAGE": "The word "+serverid+" is already exists in server"+banned},safe=False,status=status.HTTP_400_BAD_REQUEST)
    
    elif serializers.is_valid():
        serializers.save()
        return JsonResponse({"MESSAGE": "Success to Add"},safe=False, status=status.HTTP_201_CREATED)



@csrf_exempt
def banned_check(request,serverid):

    banned_info = list(models.server_banned.objects.filter(server=serverid).values())

    result=[]
    for server_ban in banned_info:
        result.append(server_ban)
    print(result,type(result))
    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)