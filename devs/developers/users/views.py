from django.shortcuts import render

# Create your views here.

def profiles(request):
    
    
    context = {}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    
    
    context = {}
    return render(request, 'users/user-profile.html', context)

def userLogin(request):
    
    context ={}
    return render(request, 'users/login-register.html', context)
    
