from django import forms
from .models import Store, StoreTable, MenuCategory, Menu, MenuOptionGroup, Option

class StoreRegistrationForm(forms.ModelForm):
    """
    店舗登録フォーム(Storeモデルに基づく)
    """
    class Meta:
        # Storeモデルをフォームのベースにする
        model = Store
        
        #A02に表示するフィールドを指定
        fields = [
            'store_name', # 店舗名
            'store_id',   # 店舗ID
            'business_number', # 事業者番号
            'owner_name', # オーナー名
            'address',    # 住所
            'telephone',  # 電話番号
            'email',      # メールアドレス
            'business_hours', # 営業時間
            'closed_days',   # 定休日
            'table_count',   # テーブル数
        ]
        
        #各FieldのWidgetを定義
        widgets = {
            'store_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: ラーメン一郎'
            }),
            'store_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: S001'
            }),
            'business_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 1234567890123'
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 山田 太郎'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 東京都足立区...'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 03-1234-5678'
            }),
            'email': forms.EmailInput(attrs={           # ← EmailInput으로 변경
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: owner@example.com'
            }),
            'business_hours': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 11:00〜21:00'
            }),
            'closed_days': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 毎週水曜日'
            }),
            'table_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors',
                'placeholder': '例: 10',
                'min': 1
            }),
        }
        
        # Fieldのラベルを定義
        labels = {
            'store_name': '店舗名',
            'store_id': '店舗ID',
            'business_number': '事業者番号',
            'owner_name': 'オーナー名',
            'address': '住所',
            'telephone': '電話番号',
            'email': 'メールアドレス',
            'business_hours': '営業時間',
            'closed_days': '定休日',
            'table_count': 'テーブル数',
        }
        
        #help textを定義
        help_texts = {
            'store_id': '英文＋数字で入力(例: S001)',
            'table_count': '店舗のテーブル数',
        }
        
class StoreTableForm(forms.ModelForm):
    """
    テーブル管理フォーム(StoreTableモデルに基づく)
    """
    class Meta:
        # StoreTableモデルをフォームのベースにする
        model = StoreTable
        # A04に表示するフィールドを指定
        fields = ['table_number', 'table_type', 'location', 'max_seats']
        # 各FieldのWidgetを定義
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl'}),
            'table_type': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl'}),
            'max_seats': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl'}),
            #'status': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl'}),
        }
        labels = {
            'table_number': 'テーブル番号',
            'table_type': 'テーブルタイプ',
            'location': '位置',
            'max_seats': '最大人数',
            #'status': 'ステータス',
        }
        
class MenuCategoryForm(forms.ModelForm):
    """
    カテゴリー管理フォーム(StoreTableモデルに基づく)
    """
    icon_image = forms.ImageField(
        required=False,
        label='アイコン画像',
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400'
        })
    )
    
    class Meta:
        model = MenuCategory
        fields = ['name', 'name_en', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: メイン料理'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: Main Course'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400'
            }),
        }
        labels = {
            'name': 'カテゴリー名',
            'name_en': '英文名',
            'display_order': '表示順',
        }
        
class MenuForm(forms.ModelForm):
    """
        A06メニュー登録・修正フォーム
    """
    class Meta:
        model = Menu
        
        fields = [
            'category',
            'name',
            'name_en',
            'price',
            'description',
            'allergy_info',
            'is_available',
            'is_sold_out',
            # img_urlはファイルアップロードのため、Viewで処理する。
        ]
        
        labels = {
            'category': 'カテゴリー',
            'name': 'メニュー名',
            'name_en': '英文名',
            'price': '価格 (円)',
            'description': '説明',
            'allergy_info': 'アレルギー情報',
            'is_available': '販売可否',
            'is_sold_out': '売切状態',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: 特製ラーメン'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': 'Example: Special Ramen'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'step': '1',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'rows': 3,
                'placeholder': '商品の説明を入力してください'
            }),
            'allergy_info': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: 小麦・卵・乳製品'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400'
            }),
        }
        
        field_classes = {
            'is_available': forms.BooleanField,
            'is_sold_out': forms.BooleanField
        }
        
    def __init__(self, *args, **kwargs):
        """
        フォームの初期化時点でstoreごとのカテゴリーだけ表示することにquerysetを制限
        """
        self.store = kwargs.pop('store', None)
        
        super().__init__(*args, **kwargs)
        if self.store:
            self.fields['category'].queryset = self.store.categories.filter(
            deleted_at__isnull=True
        ).order_by('display_order', 'name')
        
        
class OptionGroupForm(forms.ModelForm):
    """
    A07 オプショングループ登録・編集用フォーム
    """
    class Meta:
        model = MenuOptionGroup
        fields = ['menu', 'name', 'selection_type']
        labels = {
            'menu': '対象メニュー',
            'name': 'グループ名',
            'selection_type': '選択方法',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: サイズ、トッピング',
                'required': 'required'
            }),
            'selection_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'required': 'required'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.store = kwargs.pop('store', None)
        super().__init__(*args, **kwargs)
        
        if self.store:
            self.fields['menu'].queryset = Menu.objects.filter(
                store=self.store,
                deleted_at__isnull=True
            ).order_by('category__display_order', 'name')
        else:
            self.fields['menu'].queryset = Menu.objects.none()
        
        self.fields['selection_type'].choices = [
            ('single', '単一選択'),
            ('multiple', '複数選択')
        ]
        
class OptionForm(forms.ModelForm):
    """
    A08 オプション項目登録・編集用フォーム
    Viewからstoreを受け取り、現在店舗のオプショングループのみ表示する
    """
    class Meta:
        model = Option
        fields = ['menu_option_group', 'name', 'name_en', 'additional_price']
        labels = {
            'menu_option_group': 'オプショングループ',
            'name': 'オプション名',
            'name_en': '英文名',
            'additional_price': '追加価格 (円)',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: 小、中、大',
                'required': 'required'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'placeholder': '例: Small, Medium, Large'
            }),
            'additional_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:border-orange-400',
                'step': '0.01',
                'min': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        """Viewからstoreを受け取り、オプショングループを店舗限定でフィルタリング"""
        self.store = kwargs.pop('store', None)
        super().__init__(*args, **kwargs)
        
        if self.store:
            # 現在店舗のMenuOptionGroupのみ選択可能（Soft Delete除外）
            self.fields['menu_option_group'].queryset = MenuOptionGroup.objects.filter(
                menu__store=self.store,
                deleted_at__isnull=True
            ).select_related('menu').order_by('menu__name', 'name')
        else:
            self.fields['menu_option_group'].queryset = MenuOptionGroup.objects.none()
