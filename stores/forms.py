from django import forms
from .models import Store

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