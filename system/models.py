from django.db import models
from datetime import datetime

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20,db_column='user_name')
    password = models.CharField(max_length=100)
    truename = models.CharField(max_length=20,null=True,db_column='true_name')
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    is_valid = models.IntegerField(max_length=4,default=1)
    create_date = models.DateTimeField(default=datetime.now())
    update_date = models.DateTimeField(auto_now=True,null=True)
    code = models.CharField(max_length=255,null=True)
    status = models.BooleanField(max_length=1,default=0)
    timestamp = models.CharField(max_length=255,null=True,db_column='time_stamp')

    # 元信息类
    class Meta(object):
        db_table = 'user'

    def __str__(self):
        return self.username

