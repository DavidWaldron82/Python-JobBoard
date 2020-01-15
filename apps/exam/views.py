from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import *
import bcrypt

def index(request):
    return render(request,'exam/index.html')

def register(request):
    print("*"*100)
    print("this is a reg test")
    errors = Users.objects.validate(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
    else:
        hashedpw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        Users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password=hashedpw)
        user = Users.objects.last()
        request.session['logged_in'] = user.id
        print (request.session['logged_in'])
        return redirect("/dashboard")
    return redirect('/')

def login(request):
    errors = Users.objects.logVal(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
    else:
        user = Users.objects.get(email=request.POST['login_email'])
        request.session['logged_in'] = user.id
        return redirect('/dashboard')

    return redirect('/')

def dashboard(request):
    if 'logged_in' not in request.session:
        messages.error(request, "Please Login")
        return redirect('/')
    else:
        context = {
            'user': Users.objects.get(id=request.session['logged_in']),
            'job' : Jobs.objects.all()}
    return render(request, 'exam/dashboard.html', context)

def new_job(request):
    if 'logged_in' not in request.session:
        messages.error(request, "Please Login")
        return redirect('/')
    else:
        context = {'user': Users.objects.get(id=request.session['logged_in'])}
        return render(request,'exam/new_job.html', context)

def create_job(request):
    context = {'user': Users.objects.get(id=request.session['logged_in'])}
    errors = Users.objects.jobval(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
    else:
        new_job=Jobs.objects.create(title = request.POST['title'], description=request.POST['description'],location=request.POST['location'],created_by=Users.objects.get(id=request.session['logged_in']))
        return redirect('/dashboard')
    return redirect('/new_job')

def remove_job(request, job_id):
    remove_job=Jobs.objects.get(id = job_id)
    remove_job.delete()
    return redirect('/dashboard')

def edit_job(request, job_id):
    if 'logged_in' not in request.session:
        messages.error(request, "Please Login")
        return redirect('/')
    else:
        context = {
            'user': Users.objects.get(id=request.session['logged_in']),
            'job': Jobs.objects.get(id=job_id)
            }
        return render(request,'exam/edit_job.html',context)

def update_job(request, job_id):
    errors = Users.objects.jobval(request.POST)
    job_id = Jobs.objects.last().id
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit_job/{job_id}")
    else:
        edit_job=Jobs.objects.get(id = job_id)
        edit_job.title = request.POST['title']
        edit_job.description = request.POST['description']
        edit_job.location = request.POST['location']
        edit_job.save()
    return redirect('/dashboard')

def show_job(request, job_id):
    if 'logged_in' not in request.session:
        messages.error(request, "Please Login")
        return redirect('/')
    else:
        context = {'user': Users.objects.get(id=request.session['logged_in']),
        'job' : Jobs.objects.get(id=job_id)}
        return render(request,'exam/show_job.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
