from . models import Profile
from django.db.models import Q

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
        
    profiles = Profile.objects.filter(
        Q(first_name__icontains=search_query)|
        Q(last_name__icontains=search_query)|
        Q(short_intro__icontains=search_query)
    )
    
    return profiles, search_query


        
        