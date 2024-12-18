from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),
    path("user-profile/<str:pk>", views.user_profile, name="user-profile"),
    path('user-login/', views.userLogin, name='user-login'),
    path('user-register/', views.userRegister, name='user-register'),
    path('user-logout/', views.userLogout, name='user-logout'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    path('user-account/', views.userAccount, name='user-account'),
    path('msgs/', views.userMsgs, name='msgs'),
    path('read-msg/', views.read_msg, name='read-msg'),
    path('msg-details/', views.getMsgDetails, name='msg-details'),
    path('send-reply/', views.sendReply, name="send-reply")
]
