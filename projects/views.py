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
            project.save_m2m()
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
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request,'project deleted successfully')
        return redirect('account')
    context = {'delete':project}
    return render (request,'delete.html',context)

