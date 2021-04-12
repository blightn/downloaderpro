"""asynctest URL Configuration

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

from asynctest.views import index, download1, download2, download3, download4, download5

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path("download1/", download1),
    path("download2/", download2),
    path("download3/", download3),
    path("download4/", download4),
    path("download5/", download5),
]
