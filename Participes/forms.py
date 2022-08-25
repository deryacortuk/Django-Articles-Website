from django import forms 
from ckeditor.fields import RichTextFormField
from .models import Article, Comment
from mptt.forms import TreeNodeChoiceField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditorUploadingWidget())
  
    class Meta:
        DRAFTED = "DRAFTED"
        PUBLISHED = "PUBLISHED"
        STATUS_CHOICES = (
 ('DRAFTED', 'DRAFTED'),
 ('PUBLISHED', 'PUBLISHED'),
 )
        
        model = Article
        fields = ['title', 'content','tags','status','topics']
        
class CommentForm(forms.ModelForm):
    
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['parent'].widget.attrs.update(
            {'class' :'d-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['content'].label = ''
        
    class Meta:
        model = Comment
        fields = ['post', 'content', 'parent']
        widgets = {
                'content': forms.Textarea(attrs= {'class' : 'ml-3 mb-3 form-control border-0 comment-add round-0 comment-text', 'rows':'3', 'placeholder': 'What are your thoughts?',
                     'display': 'block'                               }),
              
                
            }
    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)
        
    
    
       