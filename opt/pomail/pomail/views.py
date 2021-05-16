import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from pomail.settings import EMAIL_HOST_USER
from .models import SecondaryPw
from django.contrib.auth.models import User


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "/opt/pomail/pomail/templates/send.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "/opt/pomail/pomail/templates/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "/opt/pomail/pomail/templates/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        second_pw = request.POST["second_pw"]
        second_confirm = request.POST["second_confirm"]
        if password != confirmation:
            return render(request, "/opt/pomail/pomail/templates/register.html", {
                "message": "Passwords must match."
            })

        if second_pw != second_confirm:
            return render (request, "/opt/pomail/pomail/templates/register.html", {
                "message": "Secondary Password must match."
            })
        

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, password)
            user.save()
            secondary = SecondaryPw.objects.create(user=user, secondary=second_pw)
            secondary.save()
        except IntegrityError as e:
            print(e)
            return render(request, "/opt/pomail/pomail/templates/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "/opt/pomail/pomail/templates/register.html")

def send(request):
    return render(request, "send.html", {
        "cur_mailbox": "send-mail"
    })

def SendPlainEmail(request):
    message=request.POST.get('message', '')
    subject=request.POST.get('subject', '')
    mail_id=request.POST.get('email', '')
    email=EmailMessage(subject, message, EMAIL_HOST_USER , [mail_id])
    email.content_subtype='html'
    email.send()
    return HttpResponse("Sent")

def send_mail_plain_with_stored_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'README.md')
    println(file_path)
    file=open(file_path,"r")
    email.attach("README.md", file.read(), 'text/plain')

    email.send()
    return HttpResponse("Sent")


def send_mail_plain_with_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)

    email.send()
    return HttpResponse("Sent")

@login_required
def receive_list(request, cur_page=1):
    return render(request, "/opt/pomail/pomail/templates/receive_list.html", {
        "cur_mailbox": "received-mail",
        "cur_page": cur_page,
        "tot_page": 4,
        "mail_list": [
            {
                "id": 1,
                "subject": "asdf",
                "sender": "ff@pomail.com",
                "date": "21.04.01 18:36",
                "attached": True,
                "opened": True,
            },{
                "id": 2,
                "subject": "asdf",
                "sender": "ff@pomail.com",
                "date": "21.04.01 18:36",
                "attached": False,
                "opened": False,
            },
        ],
    })


@login_required
def send_list(request, cur_page=1):
    return render(request, "/opt/pomail/pomail/templates/receive_list.html", {
        "cur_mailbox": "sent-mail",
        "cur_page": cur_page,
        "tot_page": 4,
        "mail_list": [
            {
                "id": 1,
                "subject": "asdf",
                "sender": "ff@pomail.com",
                "date": "21.04.01 18:36",
                "attached": True,
                "opened": True,
            },{
                "id": 2,
                "subject": "asdf",
                "sender": "ff@pomail.com",
                "date": "21.04.01 18:36",
                "attached": False,
                "opened": False,
            },
        ],
    })


@login_required
def read_mail(request, mail_id):
    return render(request, "/opt/pomail/pomail/templates/read_mail.html", {
        "cur_mailbox": "receive-mail",
        "mail": {
            "subject": "asdf",
            "sender": "ff@pomail.com",
            "receiver": "aa@pomail.com",
            "date": "21.04.01 18:36",
            "attached": True,
            "opened": True,
            "content": "asdf"
        },
    })