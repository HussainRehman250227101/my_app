from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from.utils import searchprofile,paginateprofiles
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, userForm,addUserForm,message_form
from .models import Profile,Skill,Message
from projects.models import Project


# LOGIN USER
def loginUser(request):
    page = 'login'
    context = {'page':page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User doesnot exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "logged in")
            return redirect(request.GET['next']  if 'next' in request.GET else 'account')
        else:
            messages.error(request, "username OR password is incorrect")
    return render(request, 'users/login_register.html',context)    

# LOGOUT USER 
def logoutUser(request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('login')


# REGISTER USER 
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.success(request, "profile created successfully")
            return redirect('edit_profile')
        else:
            messages.error(request, "An error occured while creating profile")
            
    context = {'page':page,'form':form}
    return render(request,'users/login_register.html',context)

# USER ACCOUNT 
@login_required(login_url='login')
def useraccount(request):
    profile = request.user.profile 
    projects = Project.objects.filter(owner = profile)
    skills = Skill.objects.filter(owner = profile)
    context={'profile':profile,'projects':projects,'skills':skills}
    return render(request,'users/account.html',context)

# ALL PROFILES 
def profiles(request):
    profiles, search_query = searchprofile(request) 
    custom_range,profiles = paginateprofiles(request,profiles,3)

    context = {'profiles':profiles,'search_query':search_query,'custom_range':custom_range} 
    return render(request,'users/profiles.html',context)

# EDIT PROFILE
@login_required(login_url='login')
def editprofile(request):
    profile = request.user.profile 
    form = userForm(instance=profile)
    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = form.save()
            messages.success(request, "profile updated successfully")
            return redirect('account')
        else:
            messages.error(request, "An error occured while creating profile")  
    context = {'form':form}
    return render(request, 'users/user_form.html', context)

  
# SINGLE PROFILE 
def single_profile(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.user.is_authenticated and profile == request.user.profile:
        return redirect('account')
    core_skills = profile.skill_set.exclude(description='')
    more_skills = profile.skill_set.filter(description='')
    context = {'single_profile':profile,'core_skills':core_skills, 'more_skills':more_skills}
    return render (request, 'users/single-profile.html',context)


# ADD SKILL 
@login_required(login_url='login')
def addskill(request):
    profile = request.user.profile
    form = addUserForm()
    if request.method=="POST":
        form = addUserForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully")
            return redirect('account')
    context = {'form':form}
    return render(request,'users/add_skill.html',context)


# EDIT SKILL 
@login_required(login_url='login')
def editskill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = addUserForm(instance=skill)
    if request.method=="POST":
        form = addUserForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully")
            return redirect('account')
    context = {'form':form}
    return render(request,'users/add_skill.html',context)


# DELETE SKILL 
@login_required(login_url='login')
def deleteskill(request,pk):
    
    skill = Skill.objects.get(id=pk)
    if request.method=="POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect('account')
    context = {'delete':skill}
    return render(request,'delete.html',context)

# INBOX 
@login_required(login_url='login')
def messages_inbox(request):
    profile = request.user.profile
    all_messages = profile.receiver.all()
    unread_messages_count = all_messages.filter(is_read=False).count()
    
    context ={'all_messages':all_messages,'unseen':unread_messages_count,}
    return render(request, 'users/inbox.html',context)

# SINGLE MESSAGE
@login_required(login_url='login')
def single_message(request,pk):
    profile = request.user.profile
    the_message = profile.receiver.get(id=pk)
    if the_message.is_read == False:
        the_message.is_read = True
        the_message.save()
    context={'message':the_message}
    return render(request,'users/message.html',context)

# SEND MESSAGE  
@login_required(login_url='login')
def send_message(request,pk):
    msg_receiver = Profile.objects.get(id=pk)
    form = message_form()
    if request.method=='POST':
        form = message_form(request.POST)
        if form.is_valid():
            receiver = form.save(commit=False)
            receiver.receiver = msg_receiver
            receiver.sender = request.user.profile
            receiver.save()
            messages.success(request,'Your message has been sent!')
            return redirect('single-profile',pk=msg_receiver.id)
    context={'msg_receiver':msg_receiver,'form':form}
    return render(request, 'users/message_form.html',context)