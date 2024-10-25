from django.shortcuts import render, redirect
from .models import Profile
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User

def profiles(request):
    

    context = {}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    
    
    context = {}
    return render(request, 'users/user-profile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userRegister(request):
    page = "register"
    
    form = RegistrationForm()
    if request.user.is_authenticated:
        return redirect('profiles')
    elif request.method == 'GET':
        form = RegistrationForm()
    elif request.method=='POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('profiles')
        else:
            form = RegistrationForm()
    else:
        form = RegistrationForm()
    context = {
        'page':page,
        'form':form,
    }
    return render(request, 'users/login_register.html', context)
            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userLogin(request):
    page = "login"
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        
        try:
            user = User.objects.get(username=username)
            
        except:
            print(f'The user username {username} does not exits.')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profiles')
        
        
    
    context = {
        'page':page,
    }
    return render(request, 'users/login_register.html', context)


def userLogout(request):
    logout(request)
    return redirect('user-login')   
