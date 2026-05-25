from django.urls import path
from .views import (
    StoreRegistrationView, 
    DashboardView, 
    TableManagementView, 
    TableCreateView, 
    TableUpdateView, 
    TableDeleteView, 
    CategoryManagementView, 
    CategoryCreateView, 
    CategoryUpdateView, 
    CategoryDeleteView,
    MenuCreateView,
    MenuUpdateView,
    MenuDeleteView,
)
from django.views.generic import TemplateView
from .views import MenuManagementView

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
    path('categories/', CategoryManagementView.as_view(), name='a05_category_management'),
    # CreateView 
    path('categories/create/', CategoryCreateView.as_view(), name='a05_category_create'),
    # UpdateView 
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='a05_category_update'),
    # DeleteView
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='a05_category_delete'),
    #A06 メニュー管理
    path('menus/', MenuManagementView.as_view(), name='a06_menu_management'),
    path('menus/create/', MenuCreateView.as_view(), name='a06_menu_create'),
    path('menus/<int:pk>/update/', MenuUpdateView.as_view(), name='a06_menu_update'),
    path('menus/<int:pk>/delete/', MenuDeleteView.as_view(), name='a06_menu_delete'),
]
