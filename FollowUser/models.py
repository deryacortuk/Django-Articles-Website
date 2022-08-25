from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Follow(models.Model):
    
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="following")
    
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_followers'),
            models.CheckConstraint(name="%(app_label)s_%(class)s_prevent_self_follow", check = ~models.Q(follower = models.F("following")),
            ),
        ]
        
        ordering = ['-created']
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
 
            
        
        
    
    

            

        
   
   

        

