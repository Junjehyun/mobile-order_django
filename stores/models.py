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
    
    
class StoreTable(models.Model):
    """
    A04 テーブル管理のモデル
    """
    class Status(models.TextChoices):
        VACANT = 'vacant', '空席'
        OCCUPIED = 'occupied', '使用中'
        RESERVED = 'reserved', '予約済み'
    
    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='店舗'
    )
    table_number = models.CharField(
        max_length=10,
        verbose_name='テーブル番号',
        help_text='例: 1, 2, A1, B2など'
    )
    table_type = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='テーブルタイプ',
        help_text='例: 2人用, 4人用, カウンター'
    )
    location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='位置',
    )
    qr_code_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='QRコードURL',
    )
    max_seats = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='最大人数',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.VACANT,
        verbose_name='ステータス',
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='削除日時')  # Soft Delete
    
    class Meta:
        verbose_name = 'テーブル'
        verbose_name_plural = 'テーブル一覧'
        unique_together = ('store', 'table_number')
        ordering = ['table_number']

    def __str__(self):
        return f"{self.store.store_name} - {self.table_number}"
    
class MenuCategory(models.Model):
    """
    A05 カテゴリー
    """
    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='店舗'
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name='カテゴリー名'
    )
    
    name_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='英文名'
    )
    
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='表示順'
    )
    icon_image_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='アイコン画像URL'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='削除日時')  # Soft Delete
    
    class Meta:
        verbose_name = 'メニューカテゴリー'
        verbose_name_plural = 'メニューカテゴリー一覧'
        ordering = ['display_order', 'name']
        #unique_together = ('store', 'name')  # 同じ店舗で同じ名重複防止

    def __str__(self):
        return f"{self.store.store_name} - {self.name}"
    
class Menu(models.Model):
    """
        A06 メニュー
    """
    # FK - Storeと連結
    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE,
        related_name='menus', 
        verbose_name='店舗'
    )
    
    # FK - メニューが属するカテゴリー(A05)
    category = models.ForeignKey(
        'MenuCategory',
        on_delete=models.CASCADE,
        related_name='menus',
        verbose_name='カテゴリー'
        
    )
    
    # 基本情報
    name = models.CharField(
        max_length=100,
        verbose_name='メニュー名'
    )
    
    name_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='英文名'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='価格'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='説明'
    )
    
    allergy_info = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='アレルギー情報'
    )
    
    image_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='代表イメージURL'
    )
    
    is_available = models.BooleanField(
        default=True,
        verbose_name='販売可否'
    )
    
    is_sold_out = models.BooleanField(
        default=False,
        verbose_name='売切状態'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='削除日時')  # Soft Delete
    
    class Meta:
        verbose_name = 'メニュー',
        verbose_name_plural = 'メニュー一覧',
        ordering = ['category__display_order', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.price}円)"
    
class MenuOptionGroup(models.Model):
    """
    A07 メニューオプショングループ管理
    各メニューに紐づくオプショングループ（サイズ、トッピングなど）を管理
    """
    menu = models.ForeignKey(
        'Menu',  
        on_delete=models.CASCADE,
        related_name='option_groups',  
        verbose_name='対象メニュー'
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name='グループ名'
    )
    
    selection_type = models.CharField(
        max_length=10,
        choices=[
            ('single', '単一選択'),
            ('multiple', '複数選択')
        ],
        default='single',
        verbose_name='選択方法'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='削除日時')  # Soft Delete
    
    class Meta:
        verbose_name = 'メニューオプショングループ'
        verbose_name_plural = 'メニューオプショングループ一覧'
        ordering = ['menu', 'name']
    
    def __str__(self):
        return f"{self.menu.name} - {self.name}"
    
