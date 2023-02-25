"""AI_E_Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from customerSection import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.register, name='registration'),
    path('verification/<str:token>/', views.verification, name='verification'),
    path('login/', views.attempt_login, name='login'),
    path('resetrequest/', views.request_reset, name='reset_request'),
    path('logout/', views.attempt_logout, name='logout'),
    path('deletion/', views.deletion, name='deletion'),
    path('review/', views.review, name='review'),

    path('admin/', admin.site.urls),
]
