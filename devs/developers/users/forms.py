from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Message

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=500)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
        
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','created_date']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'body')
        

class ReplyForm(ModelForm):
    class Meta:
        model=Message
        fields = ['body']

    def clean_body(self): 
        body = self.cleaned_data.get('body') 
        # Example: Strip leading and trailing whitespace 
        body = body.strip() # Add additional sanitization/validation as needed 
        if len(body) > 1000: # Example constraint 
            raise forms.ValidationError("Reply content is too long.") 
        return body