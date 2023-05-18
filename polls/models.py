from django.db import models

# Create your models here.
class slang_dict(models.Model):
    slang_text=models.CharField(max_length=200)

    def __str__(self):
        return self.slang_text

class server_user(models.Model):
    server=models.CharField(max_length=200)
    user=models.CharField(max_length=200)

    def __str__(self):
        return self.server+','+self.user
    
class server_banned(models.Model):
    server=models.CharField(max_length=200)
    banned=models.CharField(max_length=200)

    def __str(self):
        return self.server+','+self.banned
    
class user_slang_count_date(models.Model):
    server=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    date=models.DateField('date')
    count=models.IntegerField(default=0)

    def __str__(self):
        return self.server+','+self.user+','+str(self.count)+','+self.date.strftime("%Y년 %m월 %d일")
    
class user_slang_count_week(models.Model):
    server=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    year=models.IntegerField(default=0)
    week=models.IntegerField(default=0)
    count=models.IntegerField(default=0)

    def __str__(self):
        return self.server+','+self.user+','+str(self.count)

class user_sentence(models.Model):
    server=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    sentence=models.CharField(max_length=200)
    datetime=models.DateTimeField('date time')

    def __str__(self):
        return self.server+','+self.user+','+self.sentence+','+self.datetime.strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")