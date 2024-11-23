from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from .models import Message
from .forms import MessageForm

def send_emails(request):
    if request.method == "POST":
        with get_connection(
            host= settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER,  
            password=settings.EMAIL_HOST_PASSWORD,  
            use_tls=settings.EMAIL_USE_TLS 
        ) as connection:
            recipient_list = request.POST.get("email").split()  
            subject = request.POST.get("subject")  
            email_from = settings.EMAIL_HOST_USER  
            message = request.POST.get("bodyMsg")  
            print(type(recipient_list)) 
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
    
        

