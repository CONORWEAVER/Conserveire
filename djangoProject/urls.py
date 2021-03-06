"""djangoProject URL Configuration

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
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from LearningProject import views as rv


urlpatterns = [
 #   url(r'^$', views.login_redirect, name='login_redirect'),
    url(r'^$', rv.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^webapp/', include('LearningProject.urls')),
    url(r"^badges/", include("pinax.badges.urls", namespace="pinax_badges")),
]
