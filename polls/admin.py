from django.contrib import admin
from polls.models import slang_dict,server_user,server_banned,user_slang_count_date,user_sentence,user_slang_count_week
# Register your models here.

admin.site.register(slang_dict)
admin.site.register(server_user)
admin.site.register(server_banned)
admin.site.register(user_slang_count_date)
admin.site.register(user_sentence)
admin.site.register(user_slang_count_week)

