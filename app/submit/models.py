from django.db import models

from django.contrib.auth.models import User

class CodeSubmission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10)
    input_data=models.TextField(null=True,blank=True)
    output_data=models.TextField(null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    question=models.ForeignKey('home.question',on_delete=models.CASCADE)
    status=models.CharField(max_length=10,default='pending')
    

