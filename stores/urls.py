from django.urls import path
from .views import StoreRegistrationView, DashboardView, TableManagementView
from django.views.generic import TemplateView

app_name = 'stores'

urlpatterns = [
    #A02 店舗登録画面のURLパターン
    path('register/', StoreRegistrationView.as_view(), name='a02_store_register'),
    #A03 ダッシュボード画面のURLパターン
    path('dashboard/', DashboardView.as_view(), name='a03_dashboard'),
    #A04 テーブル管理画面のURLパターン
    path('tables/', TableManagementView.as_view(), name='a04_table_management'),
]