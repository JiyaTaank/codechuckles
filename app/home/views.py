from django.shortcuts import render,redirect,get_object_or_404
from home.models import question,TestCase
from django.template import loader
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from submit.views import  run_code
from submit.models import CodeSubmission
from submit.forms import CodeSubmissionForm

from django.db.models import Count,OuterRef, Subquery,Max,F,Q
from django.db.models.functions import Coalesce


# Create your views here.
@ login_required
def all_questions(request):

    query= request.GET.get('q')
    level_filter=request.GET.get('level')

    questions=question.objects.all()

    if query:
        questions=questions.filter(Q(question__icontains=query))
    
    if level_filter:
        questions=questions.filter(level=level_filter)

    context={
        'all_questions':questions,
        'query':query,
        'level_filter':level_filter,
    }

    return render(request,'all_questions.html',context)
    


@ login_required
def question_detail(request,question_id):

    question_detail=get_object_or_404(question,id=question_id)
    test_results=[]
    output=""
    status_message=""

    if(request.method=="POST"):
        form=CodeSubmissionForm(request.POST)
        if(form.is_valid()):
            
            submission=form.save(commit=False)
            submission.question=question_detail
            submission.user=request.user
            
            if request.POST.get("action")=='submit':
                test_cases=TestCase.objects.filter(question=question_detail)
                
                error_flag=False
                for test_case in test_cases:
                    test_output=run_code(submission.language,submission.code,test_case.input_data,question_detail.time_limit)

                    if "time limit exceeded" in test_output.lower():
                        test_results.append({'input': test_case.input_data, 'status': 'Time Limit Exceeded', 'is_hidden': test_case.is_hidden})
                        submission.status = "Rejected"
                        status_message = "Rejected"
                        
                        break
                    
                    elif "error" in test_output.lower():
                        test_results.append({'input': test_case.input_data, 'status': 'Error', 'is_hidden': test_case.is_hidden})
                        submission.status="Error"
                        status_message="Rejected"
                        error_flag=True
                        break

                    elif test_output.strip() == test_case.expected_output.strip():
                      test_results.append({'input': test_case.input_data, 'status': 'Passed', 'is_hidden': test_case.is_hidden})

                    else:
                      test_results.append({'input': test_case.input_data, 'status': 'Failed', 'is_hidden': test_case.is_hidden})
                      submission.status="Rejected"
                      status_message="TestCase failed"
                      break

                submission.save()
                
                all_tests_passed=all(result['status']=='Passed' for result in test_results if result['is_hidden'])

                #previous_submission=CodeSubmission.objects.filter(user=request.user,question=question_detail).order_by('-timestamp').first()

                if all_tests_passed:

                    submission.status='Accepted'                    
                    status_message="Accepted"
                else:
                    if error_flag==True:
                        output=test_output
                        status_message="Error"
                        submission.status="Rejected"
                    
                    status_message=submission.status
                
                submission.save()
                
            else:
                
                output=run_code(submission.language,submission.code,submission.input_data,question_detail.time_limit)
               
        else:
            output=""
            status_message="Invalid form submission"

        context={
        'question':question_detail,
        "form":form,
        "output":output,
        "status":status_message,
        "test_results":test_results,
    }
    else:
        form=CodeSubmissionForm()
        context={
        'question':question_detail,
        "form":form,
    }


    return render(request,'question_detail.html',context)

@login_required
def submission_detail(request, submission_id):
    
    submission = get_object_or_404(CodeSubmission, id=submission_id)
    context = {
        'submission': submission,

    }
    return render(request, 'submission_detail.html', context)

@login_required
def leaderboard(request):
    
    latest_submissions = CodeSubmission.objects.values('user', 'question').annotate(
        latest_timestamp=Max('timestamp')
    ).order_by('user', 'question')

    
    latest_submissions_ids = CodeSubmission.objects.filter(
        timestamp__in=[sub['latest_timestamp'] for sub in latest_submissions]
    ).values_list('id', flat=True)

    latest_submissions = CodeSubmission.objects.filter(id__in=latest_submissions_ids)

    
    user_data = {}

    for submission in latest_submissions:
        user_id = submission.user_id
        if user_id not in user_data:
            user_data[user_id] = {
                'username': submission.user.username,
                'total_accepted': 0,
                'latest_submission': None
            }

        if submission.status == 'Accepted':
            user_data[user_id]['total_accepted'] += 1

        if not user_data[user_id]['latest_submission'] or submission.timestamp > user_data[user_id]['latest_submission'].timestamp:
            user_data[user_id]['latest_submission'] = submission

    
    leaderboard_data = []
    for user_id, data in user_data.items():
        leaderboard_data.append({
            'username': data['username'],
            'latest_question': data['latest_submission'].question.question if data['latest_submission'] else 'N/A',
            'latest_status': data['latest_submission'].status if data['latest_submission'] else 'N/A',
            'total_accepted': data['total_accepted']
        })

    
    leaderboard_data.sort(key=lambda x: x['total_accepted'], reverse=True)

    
    for rank, entry in enumerate(leaderboard_data, start=1):
        entry['rank'] = rank

    context = {
        'leaderboard_entries': leaderboard_data,
    }

    return render(request, 'leaderboard.html', context)


def profile(request):
    user = request.user

   
    submissions = CodeSubmission.objects.filter(user=user)

    
    latest_submissions_subquery = CodeSubmission.objects.filter(
        question=OuterRef('question'),
        user=user
    ).order_by('-timestamp').values('timestamp')[:1]

    
    latest_submissions = submissions.filter(
        timestamp=Subquery(latest_submissions_subquery)
    ).order_by('question')

    
    latest_submissions_dict = {
        submission.question_id: submission
        for submission in latest_submissions
    }

   
    attempted_questions = len(latest_submissions_dict)

    
    accepted_questions = sum(
        1 for submission in latest_submissions if submission.status == 'Accepted'
    )
    rejected_questions = sum(
        1 for submission in latest_submissions if submission.status == 'Rejected'
    )
    

    question_status = []
    for q in question.objects.all():
        latest_submission = latest_submissions_dict.get(q.id, None)
        status = latest_submission.status if latest_submission else 'Not attempted'
        if status != 'Not attempted':
          question_status.append({
            'question': q,
            'status': status,
            'latest_submission': latest_submission
        })

    context = {
        'username': user.username,
        'attempted_questions': attempted_questions,
        'accepted_questions': accepted_questions, 
        'rejected_questions':rejected_questions,      
        'question_status': question_status,
    }
    return render(request, 'profile.html', context)

