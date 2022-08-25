from django.forms import fields
from Profil.models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio','linkedin_url','twitter_url','facebook_url','instagram_url']