"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from accounts.views import CustomSignupView, CustomLoginView

# accountsアプリのURLをインクルード
#from accounts import views as accounts_views

# allauthのSignupViewをインポート
from allauth.account.views import SignupView
#ログインとログアウトのURLを追加
urlpatterns = [
    path('admin/', admin.site.urls),
    # A00 REGISTER
    #path('register/', accounts_views.register_view, name='register'),
    path('register/', 
        CustomSignupView.as_view(template_name='admin/A00_register.html'), 
        name='register'),
    
    # A01 LOGIN
    # path('', LoginView.as_view(template_name='admin/A01_login.html'), name='login'),
    path('', CustomLoginView.as_view(), name='login'),
    
    # A02 STORE REGISTER
    path('stores/', include('stores.urls')),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # ログインした後のリダイレクト先を追加
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
    
    path('accounts/', include('allauth.urls')),
    
]



