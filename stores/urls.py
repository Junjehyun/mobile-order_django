from django.urls import path
from .views import StoreRegistrationView
from django.views.generic import TemplateView

app_name = 'stores'

urlpatterns = [
    #A02 店舗登録画面のURLパターン
    path('register/', StoreRegistrationView.as_view(), name='a02_store_register'),
    #A03 ダッシュボード画面のURLパターン
    path('dashboard/', TemplateView.as_view(template_name='admin/A03_dashboard.html'), name='a03_dashboard'),
]