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
from django.conf import settings
from django.conf.urls.static import static

# accountsアプリのURLをインクルード
#from accounts import views as accounts_views

# allauthのSignupViewをインポート
from allauth.account.views import SignupView
#ログインとログアウトのURLを追加
urlpatterns = [
    path('admin/', admin.site.urls),
    # REGISTER
    path('register/', 
        CustomSignupView.as_view(template_name='admin/A00_register.html'), 
        name='register'),
    
    # ログイン
    path('', CustomLoginView.as_view(), name='login'),
    
    # Store関連のURL
    path('stores/', include('stores.urls')),
    
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('accounts/', include('allauth.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



