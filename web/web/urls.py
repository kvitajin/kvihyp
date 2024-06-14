"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hypervisor_list, name='hypervisor_list'),
    path('hypervisor/<int:pk>/', views.hypervisor_detail, name='hypervisor_detail'),
    path('connections/new/', views.connection_create, name='connection_create'),
    path('proxmox/', views.proxmox_list, name='proxmox_list'),
    path('<str:hypervisor>/<str:node>/', views.vm_list, name='vm_list'),
    path('connections', views.connections, name='connections'),
    path('connections/<int:db_connection_id>', views.connections_detail, name='connections_detail'),

]
