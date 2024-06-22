from django.urls import path, include
#from two_factor.urls import urlpatterns as tf_urls

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name ="signup"),
    path("signin", views.signin, name="signin"),
    path("login", views.login_view, name="login"),
    # path("login_2f", two_factor:login) jpense la logique se fait ici car login_url existe pas dans mon dossier
    path("logout", views.logout_view, name="logout"),
    path("statistics/", views.statistics, name="statistics"),
    path("chat/", views.chat, name="chat"),
    path("otp/", views.otp_view, name="otp"),
    path("profile", views.profile_view, name = "profile")
    #path("account/", include("account.urls", namespace="account")),
    
]