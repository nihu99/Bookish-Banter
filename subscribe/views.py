from django.shortcuts import render, redirect
from BookishBanter.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail

# Create your views here.
#Send Email
def subscribe_func(request, email):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = email
        subject = 'Welcome to Bookish Banter!'
        message = 'Hope you are enjoying here!!'
        recepient = sub
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        pass

def subscribe_second_func(request,email):
    sub = email
    subject = 'Thanks for subscribing to Bookish Banter!'
    message = 'Welcome User!'
    recepient = sub
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    