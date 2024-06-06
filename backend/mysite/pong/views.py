from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "pong/homepage.html")

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("pong/homepage.html"))
    return render(request,"pong/login.html")

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("pong/homepage.html"))
    return render(request, "pong/signup.html")

def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("pong/homepage.html"))
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "pong/signin.html")


