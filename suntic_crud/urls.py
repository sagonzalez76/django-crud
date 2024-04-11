"""
URL configuration for suntic_crud project.

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
from documents import views
from django.urls import path

from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('otp/', views.otp, name='otp'),

    path('documents/', views.documents, name='documents'),

    path('documents_pending/', views.documents_pending, name='documentspending'),

    path('documents_approved/', views.documents_approved,
         name='documents_approved'),
    
    path('mydocuments/', views.documents_remitent,
         name='mydocuments'),


    path('documents/create/', views.create_document, name='create_document'),
    path('documents/<int:document_id>/',
         views.document_detail, name='document_detail'),


    path('documents/<int:document_id>/approved/',
         views.approved_document, name='approved_document'),
    path('documents/<int:document_id>/deleted/',views.deleted_document, name='deleted_document'),


    path('descargar/<int:id>/', views.descargar_archivo, name='descargar_archivo'),




]
