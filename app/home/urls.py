from django.urls import path,include
from home.views import all_questions ,question_detail,submission_detail,leaderboard,profile
from accounts.views import logout_user


urlpatterns = [
    path("questions/",all_questions,name="all-questions"),

    path("questions/<int:question_id>/",question_detail,name="question-detail"),

    path("logout/",logout_user,name="logout-user"),
    
    path("submission/<int:submission_id>/",submission_detail,name="submission-detail"),
    path("leaderboard/",leaderboard,name="leaderboard"),
    path("profile/",profile,name="profile"),    
]