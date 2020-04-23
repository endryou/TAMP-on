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
    #User based views
    UserLoginView,
    UserLogoutView,
    UserSignupView,
    UserDeleteView,
    UserUpdateView,
    UserChangePassword,

    #Main views
    HomeView,
    WelcomeView,
    NotWorkingView,

    #MailBox based views
    CreateMailBoxView,

    #Mail based views
    MailListView,
    MailDetailView,
    MailDeleteView,
    MailGetView,
    SpamListView,
    MailChangeSpamLabelView,
    )

urlpatterns = [
    #User based views
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('user-update/', UserUpdateView.as_view(), name='user-update'),
    path('user-delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user-change-password/', UserChangePassword.as_view(), name='change-password'),

    #Other views
    path('', WelcomeView.as_view(), name='welcome'),
    path('home/', HomeView.as_view(), name='home'),
    path('notworking/', NotWorkingView.as_view(), name='not-working'),

    #MailBox based views
    path('create_mailbox/', CreateMailBoxView.as_view(), name='create-mailbox'),

    #Mail based views
    path('mail_list/', MailListView.as_view(), name='mail-list'),
    path('spam_list/', SpamListView.as_view(), name='spam-list'),
    path('<int:pk>/', MailDetailView.as_view(), name='mail-detail'),
    path('<int:pk>/delete/', MailDeleteView.as_view(), name='mail-delete'),
    path('get-mail/', MailGetView.as_view(), name="get-mail"),
    path('<int:pk>/change-spam-label/', MailChangeSpamLabelView.as_view(), name='change-spam-label'),

    url(r'^', include('django.contrib.auth.urls')),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    ]