from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):

    return render(request, 'index.html')

def register(request):

    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2') :
            try:
                username = request.POST.get('username')
                user = User.objects.get(username=username)
                error = 'USer is Already Registered'
                return render(request,'error.html',{"error":error})
            except User.DoesNotExist:
                username = request.POST.get('username')
                name     = request.POST.get('name')
                email    = request.POST.get('email')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                user = User.objects.create_user(username= username, password = password1, email = email)

                newUser = UserData(user_id = user, name = name, email = email)

                newUser.save()

                dj_login(request, user)

                return redirect(dashboard)


        


    print('hello')
    return render(request,'register.html')

def login(request):

    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            auth = authenticate(username=username, password = password)

            if auth is not None:
                if auth.is_active:
                    dj_login(request,auth)
                    data = UserData.objects.get(user_id=auth)
                    return redirect(dashboard)
        except:
            error = 'User details is wrong'
            return render(request,'error.html',{'error':error})

    return render(request, 'login.html')

@login_required(login_url = 'login')
def dashboard(request):

    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)
    dj_login(request,user)

    ques = Question.objects.all()

    return render(request, 'index.html', {'data':data,'ques':ques})

@login_required(login_url = 'login')
def ques(request, pk):
    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)
    question = Question.objects.get(pk=pk)
    return render(request, 'surveypage.html',{'ques':question,'data':data})
    
@login_required(login_url = 'login')
def submit(request, pk):
    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)
    question = Question.objects.get(pk=pk)
    if request.method == "POST":
        answer = request.POST.get('answer')
        rating = request.POST.get('rating')

        answerdata = Survey(question_id=question, feedback = answer, rating=rating, user_id = data)
        answerdata.save()

        return redirect(dashboard)

@login_required(login_url = 'login')
def response(request):
    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)

    responses = Survey.objects.filter(user_id = data)
  

    return render(request,'responses.html', {'data':data, 'responses':responses})


@login_required(login_url = 'login')
def edit(request,pk):
    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)

    responses = Survey.objects.get(pk = pk)
    if request.method == "POST":
        answer = request.POST.get('answer')
        rating = request.POST.get('rating')

        responses.feedback = answer
        responses.rating = rating
        responses.save()
        return redirect(response)


    
    return render(request,'edit.html', {'data':data, 'response':responses})

def report(request,pk):
    user = User.objects.get(username = request.user)
    data = UserData.objects.get(user_id = user)

    responses = Survey.objects.get(pk = pk)
    question = Survey.objects.filter(question_id=responses.question_id)
    ques = responses.question_id.question
    count = len(question)
    rating = []
    for i in question:
        rating.append(i.rating)
    aver = sum(rating)/len(rating)
    return render(request,'report.html', {'data':data,'response_data':question,'ques':ques,'count':count,'aver':aver})



    