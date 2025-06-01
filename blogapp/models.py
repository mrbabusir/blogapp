from django.db import models
from user_manage.models import User
from datetime import datetime
from django.conf import settings
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100) # category create gareko blogs harulai
    def __str__(self):
        return self.category_name

class Blog(models.Model):
    title = models.CharField(max_length= 250) # title ko maximum length 250 rakheko
    category = models.ManyToManyField(Category,related_name='blogs') # category ko foreign key rakheko, related_name le blogs ko data lai category ma access garauna help garcha
    blogcontent = models.TextField()# blog ko content ko lagi text field rakheko textfield le unlimited length ko text store garna sakcha
    user = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id',related_name='blogs') # user ko foreign key rakheko prosgresql ma
    dateandtime = models.DateTimeField(default=datetime.now) # auto_now_add le date and time automatically sets time
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post_id = models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='comments') #related_name le comments ko data lai blog ma access garauna help garcha
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id',related_name='comments') #postgresql ma user ko foreign key rakheko., related_name le comments ko data lai user ma access garauna help garcha
    dateandtime = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return (f"{self.user},{self.post_id}")