from django.shortcuts import render, redirect
from .models import Profile
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from .utils import searchProfiles
from extras import paginateObject
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProfileForm


def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateObject(request, profiles)
    
    context={
        'search_query':search_query, 
        'profiles':profiles,
        'custom_range':custom_range
    }
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(userid=pk)
    
    context = {'profile':profile}
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

@login_required(login_url="user-login")
def userAccount(request):
    profile = request.user.profile
    
    context = {'profile':profile}
    return render(request, 'users/user-account.html', context)


@login_required(login_url='user-login')
def updateProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    
    context = {
        'form':form,
    }
    return render(request, 'users/update_profile.html', context)
    

def userMsgs(request):
    
    context ={}
    return render(request, 'users/messages.html', context)