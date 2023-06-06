from django import urls
from django.urls import path, include

from . import views

urlpatterns=[
    path('<serverid>/<userid>/sentence/',views.check_sentence,name='check_sentence'),
    path('<serverid>/<userid>/count_date/<int:year>/<int:month>/<int:day>',views.user_count_date,name='user_count_date'),
    path('<serverid>/<userid>/count_week/<int:year>/<int:week>',views.user_count_week,name='user_count_week'),
    path('<serverid>/count_date/<int:year>/<int:month>/<int:day>',views.server_count_date,name='server_count_date'),
    path('<serverid>/count_week/<int:year>/<int:week>',views.server_count_week,name='server_count_week'),
    path('storeban/',views.store_ban,name='storeban'),
    path('storeslang/',views.store_slang,name='storeslang'),
    path('storeuser/',views.store_user,name='storeuser'),
    path('storecountdate/',views.store_count_date,name='storecountdate'),
    path('storecountweek/',views.store_count_week,name='storecountweek'),
    path('storesentence/',views.store_sentence,name='storesentence'),
    path('<serverid>/banned_check/',views.banned_check,name='banned_check'),
    path('', views.home, name='home'),
]