from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Skill,Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        labels = {
            'first_name':'Name'
        }

    
    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        for value in self.fields.values():
            value.widget.attrs.update({'class':'input input--text'})


class userForm(ModelForm):
    class Meta:
        model = Profile
        fields =['name','email','username','location','short_intro','bio','profile_image',
                 'social_github','social_twitter','social_linkedin','social_youtube','social_website']

    def __init__(self,*args,**kwargs):
        super(userForm,self).__init__(*args,**kwargs)
        for value in self.fields.values():
            value.widget.attrs.update({'class':'input input--text'})

class addUserForm(ModelForm):
    class Meta:
        model = Skill
        fileds = "__all__"
        exclude = ['owner']
    
    def __init__(self,*args,**kwargs):
        super(addUserForm,self).__init__(*args,**kwargs)
        for value in self.fields.values():
            value.widget.attrs.update({'class':'input input--text'})


class message_form(ModelForm):
    class Meta:
        model = Message
        fields = ['subject','body']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for value in self.fields.values():
            value.widget.attrs.update({'class':'input input--text'})