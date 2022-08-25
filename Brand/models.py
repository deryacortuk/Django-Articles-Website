from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class BrandModel(models.Model):
    brand = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(db_index=True)
    
    
    class Meta:
        ordering = ['brand']
        
    def __str__(self):
        return self.brand
    
    def get_absolute_url(self):
        return reverse("brands:brand", args = [self.slug ])
    @property     
    def structured_data(self):
        data = {
            "@context": "https://schema.org",
            "@type": "Organization",
             "name": self.brand,
            "url" :"brands/"+self.slug
             
             
        }
        
        return data
    
class BrandEntry(models.Model):  
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_entry')
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE ,related_name='brand_comments')
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    heart_like = models.IntegerField(default = 0)
    hands_like = models.IntegerField(default = 0)
    star_like = models.IntegerField(default = 0)
    
    
    class Meta:
        ordering = ['created']
        
    def __str__(self):
        return str(self.brand)
   
   
    

    
    
