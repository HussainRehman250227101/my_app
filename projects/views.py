from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import searchproject,paginateprojects
from .models import Project,Review
from users.models import Profile
from .forms import project_form,review_form




def projects(request):
    projects,search_query = searchproject(request)
    custom_range,projects = paginateprojects(request,projects,6)

    
    context ={'projects': projects,'search_query':search_query , 'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def single_project(request, pk):
    project = Project.objects.get(id=pk)
    review = project.review_set.all()
    form = review_form()
    if request.method=='POST':
        form = review_form(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile 
        review.project = project
        review.save()
        project.reviews_count
        messages.success(request,'Your review was added successfully')
        return redirect('project',pk = project.id)

    reviewers = project.reviewers
    
    context = {'project':project,'reviews':review,'form':form,'reviewers_id_list':reviewers}
    return render(request,'projects/single-project.html', context)

@login_required(login_url='login')
def addproject(request):
    profile = request.user.profile
    form = project_form()
    if request.method == 'POST':
        form= project_form(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save_m2m()
            messages.success(request,'project added successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/add_project.html',context)

@login_required(login_url='login')
def editproject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = project_form(instance=project)
    if request.method == 'POST':
        form= project_form(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,'project updated successfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/edit_project.html',context)

@login_required(login_url='login')
def deleteproject(request,pk):
    prev_url = request.META.get('HTTP_REFERER','/')
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request,'project deleted successfully')
        return redirect('account')
    context = {'delete':project,'prev_url':prev_url}
    return render (request,'delete.html',context)

@login_required(login_url='login')
def edit_review(request,pk):
    prev_url = request.META.get('HTTP_REFERER','/')
    profile = request.user.profile 
    project = Project.objects.get(id=pk)
    review = profile.review_set.get(project__id = pk)
    form = review_form(instance= review)
    if request.method =='POST':
        form = review_form(request.POST,instance = review)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = profile 
            inst.project = project 
            inst.save()
            project.reviews_count
            messages.success(request,'review updated successfully')
            return redirect('project',  pk=pk)
    context = {'form':form,'prev_url':prev_url,'review':review}
    return render(request,'projects/edit_review.html',context) 

def delete_review(request,pk):
    review = request.user.profile.review_set.get(id=pk)
    project = review.project
    context = {'delete':review}
    if request.method =='POST':
        review.delete()
        project.reviews_count 
        messages.success(request,'review deleted successfully')
        return redirect('project' , pk = review.project.id)

    return render(request,'delete.html',context)