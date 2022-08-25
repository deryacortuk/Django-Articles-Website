from django import forms
from .models import DailyModel, DailyComment
from mptt.forms import TreeNodeChoiceField


class DailyForm(forms.ModelForm):
    
    class Meta:
        model = DailyModel
        
        fields = ['content']
        
class CommentDailyForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=DailyComment.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update(
            {'class' :'d-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['content'].label = ''
    class Meta:
        model = DailyComment
        fields = ['post','content','parent']
        widgets = {
                'content': forms.Textarea(attrs= {'class' : 'ml-3 mb-3 form-control border-0 comment-add round-0 comment-text', 'rows':'7', 'placeholder': 'What are your thoughts?',
                     'display': 'block'                               }),
              
                
            }
    def save(self, *args, **kwargs):
        DailyComment.objects.rebuild()
        return super(CommentDailyForm, self).save(*args, **kwargs)

    
