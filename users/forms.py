from django import forms
from .models import PersonalDetails
from django.forms import ModelForm,HiddenInput,Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
class PresonalDetailsForm(ModelForm):
    class Meta:
        model=PersonalDetails
        fields='__all__'#['age','blood_group']

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    def save(self,commit=False):
        user = super(UserRegistrationForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user #creates a new instance of the form and saves it to db
class UserUpdateForm(ModelForm):
    class Meta:
        model=User
        fields=['username', 'email' ]
class ProfileUpdateForm(ModelForm):
    class Meta:
        model=PersonalDetails
        fields=['age','blood_group']

class UserLoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(UserLoginForm,self).__init__(*args,**kwargs)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
class OrderForm(forms.Form):
    pharma_name=forms.CharField(label='pharmacy')
    medicine_name=forms.CharField()
    quantity=forms.IntegerField()
    delivery_address=forms.CharField(widget=Textarea)
    phone_no=forms.CharField(label='phone number')
    image=forms.ImageField(label='upload the prescription',required=True)
    pharma_email=forms.EmailField(widget=HiddenInput)