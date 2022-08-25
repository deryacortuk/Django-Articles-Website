
from .models import Follow
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify



# Create your views here.

@require_POST
@login_required
@csrf_exempt
def follow(request):
    user_id = request.POST.get('id', None)
    action = request.POST.get('action', '')
    
    if user_id and action:
        try:
            user = User.objects.get(id = user_id)
            if action == "follow":
                
                Follow.objects.get_or_create(follower = request.user, following = user)
               
                if request.user != user:
                        notify.send(request.user, recipient = user, verb="started following you")
                               
                
                                              
                
            else:
                Follow.objects.filter(follower = request.user, following = user).delete()
            
            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status' : 'error'})
    return JsonResponse({'status': 'error'})


