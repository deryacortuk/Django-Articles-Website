from django import forms

from .models import BrandEntry
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class BrandForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditorUploadingWidget())
    class Meta: 
        
        model = BrandEntry
        fields = [ 'content']