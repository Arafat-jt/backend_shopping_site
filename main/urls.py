"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings
from . import views

urlpatterns = [
    path("men/", views.func_men, name="men's list"),
    path("women/", views.func_women, name="women's list"),
    path("userlogin/", views.user_login, name="user login"),
    path("usersignup/", views.user_signup, name="user sign up"),
    path("", views.index, name="go no where"),
]