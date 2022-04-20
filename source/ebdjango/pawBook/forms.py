import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pawBook.models import SocialPost, WeatherPost, DogPost

class NewUserForm(UserCreationForm):
   email = forms.EmailField(required=True)

   class Meta:
      model = User
      fields = ("username", "email", 'password1', 'password2')

      def save(self, commit=True):
         user = super(NewUserForm, self).save(commit=False)
         user.email = self.cleaned_data['email']
         if commit:
            user.save()
         return user

class SocialPostForm(forms.ModelForm):
   class Meta:
      fields = ("title", "content",)
      model = SocialPost



class WeatherPostForm(forms.ModelForm):
   class Meta:
      fields = ["title", "location",]
      model = WeatherPost

class DogPostForm(forms.ModelForm):
   class Meta:
      fields = ["title", "content"]
      model = DogPost