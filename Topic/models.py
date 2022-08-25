from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(db_index=True )
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("topic:topic",args=[self.slug])
    
    @property     
    def structured_data(self):
        data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
             "name": self.title,
            "url" :"topic/"+self.slug
             
             
        }
        
        return data
    
