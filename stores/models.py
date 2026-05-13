from django.db import models

# Create your models here.

from accounts.models import CustomUser

class Store(models.Model):
    """
    A02で入力するすべての情報を保存する。
    OwnerはCustomUserモデルのユーザーと1対1の関係を持つ。
    Manager, StaffはCustomUserモデルのユーザーと多対多の関係を持つ。
    """
    
    owner = models.OneToOneField(
        CustomUser, # CustomUserモデルを参照
        on_delete=models.SET_NULL, # オーナーが削除された場合、店舗は削除せずにオーナーをNULLにする
        null=True,
        blank=True,
        related_name='owned_store', # CustomUserからStoreへの逆参照名
        verbose_name='オーナー'
    )
    
    store_name = models.CharField(
        max_length=100,
        verbose_name='店舗名'
    )
    
    store_id = models.CharField(
        max_length=20,
        unique=True, # 店舗IDは一意である必要がある
        null=True,
        blank=True,
        verbose_name='店舗ID'
    )
    
    business_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='事業者番号'
    )
    
    owner_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='代表者名'
    )
    
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='住所'
    )
    
    telephone = models.CharField(
        max_length=20,
        verbose_name='電話番号'
    )
    
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='メールアドレス'
    )
    
    business_hours = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='営業時間',
        help_text='例: 11:00-22:00'
    )
    
    closed_days = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='定休日',
        help_text='例: 毎週水曜日'
    )
    
    table_count = models.PositiveIntegerField(
        verbose_name='テーブル数',
        help_text='例: 10'
    )
    
    # 自動管理フィールド
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="削除日時")  # Soft Delete
    
    class Meta:
        verbose_name = '店舗'
        verbose_name_plural = '店舗'
        db_table = 'stores'  # データベーステーブル名を指定
        ordering = ['-created_at']  # 作成日時の降順で並び替え
        
    def __str__(self):
        return self.store_name