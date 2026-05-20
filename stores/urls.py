from django.urls import path
from .views import StoreRegistrationView, DashboardView, TableManagementView, TableCreateView, TableUpdateView, TableDeleteView
from django.views.generic import TemplateView

app_name = 'stores'

urlpatterns = [
    #A02 店舗登録画面のURLパターン
    path('register/', StoreRegistrationView.as_view(), name='a02_store_register'),
    #A03 ダッシュボード画面のURLパターン
    path('dashboard/', DashboardView.as_view(), name='a03_dashboard'),
    #A04 テーブル管理画面のURLパターン
    path('tables/', TableManagementView.as_view(), name='a04_table_management'),
        path('tables/create/', TableCreateView.as_view(), name="a04_table_create"), #A04 新規テーブル登録のURLパターン
            path('tables/<int:pk>/update/', TableUpdateView.as_view(), name="a04_table_update"), #A04 テーブル更新のURLパターン
                path('tables/<int:pk>/delete/', TableDeleteView.as_view(), name='a04_table_delete'),
    #A05 メニューカテゴリー管理画面のURLパターン
]