from django.shortcuts import render, redirect
from .models import Profile, Message
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from .utils import searchProfiles
from extras import paginateObject
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProfileForm, MessageForm, ReplyForm
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.core.mail import EmailMessage, get_connection
from django.conf import settings



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

    form = MessageForm()

    if request.user.is_anonymous:
        sender = None
    else:
        try:
            sender = request.user.profile 
        except User.DoesNotExist:
            sender = None
    #print(f'User is : {sender}')
    
    if request.method == "POST":
        form =MessageForm(request.POST)
        if form.is_valid():

            message = form.save(commit=False)
            message.name = form.cleaned_data['name']
            message.email = form.cleaned_data['email']
            message.subject = form.cleaned_data['subject']
            message.body = form.cleaned_data['body']

            # When user is not authenticated.
            message.sender = sender
            message.recipient = profile

            # When user is authenticated 
            if sender:
                message.name = sender.first_name +' '+ sender.last_name
                message.email = sender.email
            
            message.save()

    context = {
        'profile':profile,
        'form':form
        }
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
    
@login_required(login_url='user-login')
def userMsgs(request):
    profile = request.user.profile
    msgsRecipient = Message.objects.filter(recipient=profile)
    msgsSender = Message.objects.filter(sender=profile)
    unreadCount = msgsRecipient.filter(is_read=False).count()
    
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            msgsRecipient.sender = request.user
            form.save()
            return redirect('msgs')
        else:
            form = MessageForm()
   
    #Send Emails

    #send_emails(request)

    context ={
        'msgsRecipient':msgsRecipient,
        'msgsSender':msgsSender,
        'unreadCount':unreadCount, 
    }
    return render(request, 'users/messages.html', context)


@login_required(login_url='user-login')
@require_POST
def read_msg(request):
    import json
    profile = request.user.profile
    data = json.loads(request.body)
    msgid = data.get('msgid')
    #print(f'This, {msgid}, should not be empty.')
    #print(f'Parsed data {data}, Type: {type(data)}')
    if msgid:
        try:
            msg = Message.objects.get(id=msgid)
            msg.is_read = True
            msg.save()
            unreadCount = Message.objects.filter(recipient=profile, is_read=False).count()
            #print(f'Returning response with unreadCount {unreadCount}')
            return JsonResponse({
                'status':'success',
                'unreadCount' : unreadCount
            })
        except Message.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message':'Message not found'
            }) 
    return JsonResponse({
                'status':'error',
                'message':'Invalid request'
            })
          

@require_GET
def getMsgDetails(request):
    #import json
    #data = json.loads(request.body)
    #msgid = data.get('msgid')
    msgid = request.GET.get('msgid')
    if msgid:
        try:
            msg = Message.objects.get(id=msgid)
            return JsonResponse({
                'subject': msg.subject,
                'senderEmail': msg.email,
                'senderName':msg.name,
                'recipientName':msg.recipient.first_name +' '+ msg.recipient.last_name,
                'recipientEmail': msg.recipient.email,
                'body': msg.body,
                'created' : msg.created.strftime('%Y-%m-%d, %H:%M:%S'),
                'picture' : msg.sender.profile_image.url if msg.sender else 'profiles/user-default.png'
            })
        except Message.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message':'Message not found'
            }) 
    return JsonResponse({
                'status':'error',
                'message':'Invalid request'
            })

@require_POST
def sendReply(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        reply_body = data.get('replyContent')
        
        msgid = data.get('msgid')
        print(f'id = {msgid}')
        try:
            parent_message = Message.objects.get(id=msgid)
            recipientEmail = parent_message.email
            user = User.objects.get(email=recipientEmail)
            #print(f'parent: {parent_message},  id= {msid}')
            form = ReplyForm({'body': reply_body})

            if form.is_valid():
                reply_msg = form.save(commit=False)
                reply_msg.sender = request.user.profile
                reply_msg.recipient = parent_message.sender
                reply_msg.subject = f'Re: {parent_message.subject}'
                reply_msg.body = form.cleaned_data['body']
                reply_msg.parent = parent_message
                reply_msg.save()

                return JsonResponse({
                    'status': 'success',
                    'reply_id': reply_msg.id
                })
            else:
                return JsonResponse({
                    'status':'errors',
                    'message':'Invalid data',
                    'errors':form.errors
                }, status=400)
        except User.DoesNotExist:
            #Send reply to non users. 
            print('User does not exist.')
        except Message.DoesNotExist:
            return JsonResponse({
                'status':'error',
                'message':'Message not found'
            }, status=400)
    return JsonResponse({
                'status':'error',
                'message':'Invalid method'
            }, status=400)

