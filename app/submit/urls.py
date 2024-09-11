from django.urls import path
from submit.views import run_code 
app_name="submit"

urlpatterns=[
    path("<int:question_id>/",run_code,name="pre-run" ),
]
