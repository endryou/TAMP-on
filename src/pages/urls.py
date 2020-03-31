"""tampon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include as url_include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomeView,
    LoginView,
    LogoutView,
    RegisterView,
    SignupView,
    WelcomeView,

    MailBoxView,
    MailDetailView,
    MailDeleteView,

    CreateMailBoxView,

    ProbaGmaila
    )

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', WelcomeView.as_view(), name='welcome'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('home/', HomeView.as_view(), name='home'),
    path('proba/', ProbaGmaila.as_view(), name='proba'),

    path('create_mailbox/', CreateMailBoxView.as_view(), name='create-mailbox')

    path('', MailBoxView.as_view(), name='mail-list'),
    path('<int:pk>/', MailDetailView.as_view(), name='mail-detail'),
    path('<int:pk/delete/', MailDeleteView.as_view(), name='mail-list'),

    url(r'^', include('django.contrib.auth.urls')),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    ]