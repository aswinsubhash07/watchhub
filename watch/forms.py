
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from watch.models import UserProfile




class SignupForm(UserCreationForm):

    password1=forms.CharField(widget=(forms.TextInput(attrs={"class":"border-1 peer block w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-2.5 pt-4 pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"})))
    password2=forms.CharField(widget=(forms.PasswordInput(attrs={"class":"border-1 peer block w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-2.5 pt-4 pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"})))

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":"border-1 peer block w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-2.5 pt-4 pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0 "}),
            "email":forms.EmailInput(attrs={"class":"border-1 peer block w-full appearance-none rounded-lg border border-gray-300 bg-transparent px-2.5 pt-4 pb-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"}),
           
        }

class SiginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full flex-1 appearance-none border-gray-300 bg-white py-2 px-4 text-base text-gray-700 placeholder-gray-400  focus:outline-none"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"w-full flex-1 appearance-none border-gray-300 bg-white py-2 px-4 text-base text-gray-700 placeholder-gray-400  focus:outline-none"}))

class UserProfileForm(forms.ModelForm):
    class Meta:

        model=UserProfile
        fields=["bio","profile_pic"]
        widgets={
            "bio":forms.TextInput(attrs={"class":"form-control"}),

            "profile_pic":forms.FileInput(attrs={"class":'form-control'}),

        }