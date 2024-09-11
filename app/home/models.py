from django.db import models
from django.contrib.auth.models import User

class question(models.Model):

    question=models.CharField(max_length=300)
    level=models.CharField(max_length=20)    
    description=models.TextField(max_length=2000,default="no description")
    example_output=models.TextField(max_length=1000,default="no example")
    example_input=models.TextField(max_length=1000,default="no example")
    time_limit=models.FloatField(default=1.0)
    constraint_n=models.TextField()
    
class TestCase(models.Model):
    question = models.ForeignKey('home.question', on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=True)



    


