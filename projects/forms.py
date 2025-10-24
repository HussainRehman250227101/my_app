from django.forms import ModelForm
from django import forms
from .models import Project,Review

class project_form(ModelForm):
    class Meta:
        model = Project
        fields = ['title','image','Description','tags','demo_link','source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(project_form,self).__init__(*args,**kwargs)
        for key,value in self.fields.items():
            value.widget.attrs.update({'class':'input input--text'})

class review_form(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        
        labels = {
            'value':'Place your Vote',
            'body': 'Write a Review to your Vote'
        }
    def __init__(self,*args,**kwargs):
        super(review_form,self).__init__(*args,**kwargs)
        for key,value in self.fields.items():
            value.widget.attrs.update({'class':'input input--text','style': 'width: 100% !important;'})
            

