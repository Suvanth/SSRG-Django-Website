from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, FileResponse
from .forms import NewUser, SubmitJob, Files
from .models import Jobs, SingleFiles
from subprocess import run, PIPE
import os, sys
from SSRG.celery import testTask

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'MossBackendJobs/jobRequest.py')

filename2 = os.path.split(dirname)
filename2 = os.path.join(filename2[0], 'jobs')

# Create your views here.
def homepage(request):
    return render(request=request, template_name='Jobs/home.html')

def menu(request):
    return render(request=request, template_name='Jobs/menu.html')

def registerRequest(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Success")
            return redirect("menu")
        messages.error(request, "Error! Invalid information")
    form = NewUser()
    return render(request = request, template_name="Jobs/register.html", context={'registration':form})

def loginRequest(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Login successful. Welcome {username}!")
                return redirect("menu")
            else:
                messages.error(request, "Invalid Username/Password combination")
        else:
            messages.error(request, "Invalid Username/Password combination")

    form = AuthenticationForm()
    return render(request=request, template_name="Jobs/login.html", context={'login':form})

def logoutRequest(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("homepage")

def newJob(request):
    #form = SubmitJob()
    basefileState = 'False'
    if request.method == 'POST':
        form = SubmitJob(request.POST)
        singleFilesForm = Files(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid() and singleFilesForm.is_valid():
            job = form.save(commit=False)
            form.instance.user = request.user
            job.save()
            for f in files:
                fileInstance = SingleFiles(files = f, jobInstance = job, user=request.user, slug = form.instance.slug)
                fileInstance.save()
            files = request.FILES.getlist('baseFile')
            if (len(files)==0):
                basefileState = 'False'
            else:
                basefileState = 'True'
            for f in files:
                fileInstance = SingleFiles(baseFile = f, jobInstance = job, user=request.user, slug = form.instance.slug)
                fileInstance.save()


            arguments = [form.instance.user.username, 
                        form.instance.language,
                        basefileState, 
                        form.instance.user.email,
                        form.instance.emailNow,
                        form.instance.slug,
                        f"{filename2}/{form.instance.user.username}/{form.instance.slug}"]
            #job.save()
            testTask.delay(filename, arguments[0], arguments[5], arguments[1], arguments[2], arguments[3], arguments[4], arguments[6])

            #form.instance.jobState = 'done'
            #job.save()
            
            return redirect("menu")
    else:
        form = SubmitJob()
        singleFilesForm = Files()
    return render(request=request, template_name="Jobs/newJob.html", context={'submission': form, 'singles':singleFilesForm})

def viewJobs(request):
    return render(request=request, template_name="Jobs/jobsSubmitted.html", context={'pendingJobs':Jobs.pendingJobObjects.filter(user=request.user), 'successJobs':Jobs.successJobObjects.filter(user=request.user), 'failedJobs':Jobs.failedJobObjects.filter(user=request.user)})

def singleJobDetail(request, jobs):

    jobs = get_object_or_404(Jobs, slug=jobs)
    return render(request=request, template_name="Jobs/jobDetails.html", context={'jobs':jobs})

def reportView(request, jobs):
    path = os.path.split(dirname)
    path = os.path.join(path[0], 'jobs')
   
    reportPath = f"{path}/{request.user}/{jobs}/JobReport.pdf"
    return FileResponse(open(reportPath, 'rb'), content_type='application/pdf')
