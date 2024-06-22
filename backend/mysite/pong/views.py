from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from base64 import b64encode
from django.core.files.base import ContentFile
from .utils import send_otp
from .models import NewUser, Tournament, Party, Chat, Message, Statistic, Participant, Friendship, BlockedUser
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import pyotp
import qrcode
from io import BytesIO
import base64
 
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "pong/homepage.html")
    #return render(request, "pong/index.html")

def login_view(request):
    if not request.user.is_authenticated:
        return render(request,"pong/login.html")
    else:
        #ça serait bien de rajouter une notification "vous êtes déjà connecté"
        return HttpResponseRedirect(reverse("index"))


def signup(request):
    if request.user.is_authenticated:
        #ça serait bien de rajouter une notification "vous êtes déjà connecté"
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        avatar = request.FILES.get("avatar")
        pseudo = request.POST.get("pseudo")

        if NewUser.objects.filter(pseudo=pseudo).exists():
            return render(request, 'pong/signup.html', {
                'error_message': "Username already exists. Please choose a different pseudo."
            })

        
        if NewUser.objects.filter(email=email).exists():
            return render(request, 'pong/signup.html', {
                'error_message': "Email already exists. Please choose a different email."
            })
        binary_data = b64encode(avatar.read())

        user = NewUser.objects.create_user(email=email, password=password, pseudo=pseudo, avatar=binary_data)
        user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "pong/signup.html")
        

def signin(request):
    if request.user.is_authenticated:
        #ça serait bien de rajouter une notification "vous êtes déjà connecté"
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # login(request, user)
            request.session['user_id'] = user.id
            if user.is_mfa_enabled is True:
                #send_otp(request)
                #request.session["email"] = email
                return redirect("otp")
            else:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "pong/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "pong/signin.html")
#faire la ologique du otp sur la view otp avec la comparaison du code que le mec aura recu (comme il a deja scanné)
def otp_view(request):
    user = NewUser.objects.get(id=(request.session.get('user_id')))
    message = 'nothing'
    value = False
    if request.method == "POST":
        otp = request.POST["otp"]
        totp = pyotp.TOTP(user.mfa_hash) #check the secret key
        if totp.verify(otp): # the case where we can login the user
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else: # le cas où la secret key n'est pas la bonne
            value = True
            message = 'invalid one time password or the password has expired'      
    return render(request, 'pong/otp.html' , {
                                                'error_message' : {
                                                                        'value' : value,
                                                                        'message' : message
                                                                }
                                            })

def statistics(request):
    # return HttpResponseRedirect(reverse("pong:chat.html"))
    return render(request, "pong/statistics.html")

def chat(request):
    return render(request, "pong/chat.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def profile_view(request):
    user = NewUser.objects.get(id=(request.session.get('user_id')))
    url = pyotp.totp.TOTP(user.mfa_hash).provisioning_uri(name=user.email, issuer_name="Pong")
    qr = qrcode.make(url)
    buffered = BytesIO()
    qr.save(buffered)
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    test_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/yrdW3QAAAAASUVORK5CYII="
    if request.method == "POST":
        choice = request.POST.get("options")
        if choice == "enabled":
            user.is_mfa_enabled = True
            user.save()
        else:
            user.is_mfa_enabled = False
            user.save()
    return render(request, "pong/profile.html", {
                                                        'user_info' : {
                                                            'user_choice' : user.is_mfa_enabled,
                                                            'user_url'    : qr_base64
                                                            } 
                                                    })


