from django.shortcuts import render

# Create your views here.
# A02 店舗登録画面のビュー
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Store
from .forms import StoreRegistrationForm, StoreTableForm #forms.pyからStoreRegistrationFormとStoreTableFormをインポート
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StoreTable
from django.contrib import messages
from django.utils import timezone

class StoreRegistrationView(LoginRequiredMixin, CreateView):
    """
    A02 店舗登録画面を処理するViewクラス
    ログイン必須
    storeがすでに存在する場合はA03にリダイレクト
    Storeモデル + StoreRegistrationFormを使用
    """
    
    #基本設定
    model = Store # どんなモデルでCreateViewを作るか
    form_class = StoreRegistrationForm # どんなフォームを使うか
    template_name = 'admin/A02_store_register.html' # どのテンプレートを使うか
    success_url = reverse_lazy('stores:a03_dashboard') # 登録成功後のリダイレクト先 (dashboardに設定)
    
    # アクセス制御
    def dispatch(self, request, *args, **kwargs):
        """
        ページにアクセスする時に呼ばれるメソッド
        すでにStoreが存在する場合はA03にリダイレクト
        A02はstore_idがNULLの場合のみ表示されるべき
        """
        if request.user.is_authenticated and request.user.store is not None:
            return redirect('stores:a03_dashboard') # すでにStoreがある場合はA03にリダイレクト
        
        #storeがないユーザーだけ、A02画面を表示
        return super().dispatch(request, *args, **kwargs)
    
    # 登録成功後の処理
    def form_valid(self, form):
        """
        ユーザーがフォームを入力して、登録ボタンを押したときに実行
        1. Storeオブジェクトを生成(まだDBには保存しない)
        2. 現在ログインしたユーザーをStoreのownerに設定
        3. StoreオブジェクトをDBに保存
        4. CustomUserのstoreフィールドにも連結(N:1のリレーションを保存)
        5. サクセスメッセージを表示して、A03にリダイレクト
        """
        # formからStoreオブジェクトを生成(まだDBには保存しない)
        store = form.save(commit=False)
        
        # 現在ログインしているユーザーをStoreのownerに設定 (1:1のリレーション)
        store.owner = self.request.user
        store.save() # StoreオブジェクトをDBに保存
        
        # CustomUserのstoreフィールドにも連結 (N:1のリレーションを保存)
        # 後でManagerやStaffも同じStoreに所属する可能性があるため、ユーザーのstoreフィールドを更新
        user = self.request.user
        user.store = store
        user.save(update_fields=['store']) # storeフィールドだけ更新
        
        # Djangoが自動的に Success_urlにリダイレクトする。
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        登録しっぱいしたときに呼ばれるメソッド
        - エラーメッセージをユーザーに表示するため、super()呼び出す。
        - ここでカスタムメッセージ追加可能
        """
        return super().form_invalid(form)
        
class DashboardView(LoginRequiredMixin, TemplateView):
    """A03 ダッシュボード画面を処理するViewクラス"""
    template_name = 'admin/A03_dashboard.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        user = request.user
        # StoreがないユーザーはA02にリダイレクト
        if not hasattr(user, 'store') or user.store is None:
            return redirect('stores:a02_store_register')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.request.user.store

        context['store'] = store
        context['user'] = self.request.user

        tables = StoreTable.objects.filter(
            store=store,
            deleted_at__isnull=True
        )

        context['table_summary'] = {
            'total': tables.count(),
            'vacant': tables.filter(status='vacant').count(),
            'occupied': tables.filter(status='occupied').count(),
            'reserved': tables.filter(status='reserved').count(),
        }

        context['tables'] = tables  

        context['recent_orders'] = []
        context['sales_summary'] = {
            'today': 0,
            'order_count_today': 0,
        }

        return context
    
class TableManagementView(LoginRequiredMixin, TemplateView):
    """A04 テーブル管理画面を処理するViewクラス
    テーブルの一覧表示、テーブルの状態変更(空席/使用中/予約)を処理
    """
    template_name = 'admin/A04_table_management.html'
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        user = request.user 
        if not hasattr(user, 'store') or user.store is None:
            return redirect('stores:a02_store_register')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.request.user.store
        
        #現在の店舗のテーブルをすべて取得
        context['tables'] = StoreTable.objects.filter(
            store = store,
            deleted_at__isnull=True
        ).order_by('table_number')
        
        return context
    
class TableCreateView(LoginRequiredMixin, CreateView):
    """A04 新規テーブル登録を処理する"""
    
    # StoreTableモデルを使用
    model = StoreTable
    # StoreTableFormを使用
    form_class = StoreTableForm
    template_name = 'admin/A04_table_management.html' #同じA04のモーダルで処理する
    success_url = reverse_lazy('stores:a04_table_management') #登録成功後はA04にリダイレクト
    
    def form_valid(self, form):
        form.instance.store = self.request.user.store # 現在のユーザーの店舗をテーブルのstoreフィールドに設定
        instance = form.save()
        from .utils import generate_qr_code
        generate_qr_code(instance)
        messages.success(self.request, 'テーブルを登録しました。') # 登録成功のメッセージを追加
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # A04のテーブル管理画面のコンテキストを取得
        store = self.request.user.store # 現在のユーザーの店舗を取得
        # 現在の店舗のテーブルをすべて取得して、コンテキストに追加
        context['tables'] = StoreTable.objects.filter(
                store=store, deleted_at__isnull=True
            ).order_by('table_number')
        return context
        
class TableUpdateView(LoginRequiredMixin, UpdateView):
    """ A04 テーブル編集を処理する """
    model = StoreTable # 編集対象のモデルはStoreTable
    form_class = StoreTableForm # StoreTableFormを使用
    template_name = 'admin/A04_table_management.html' #同じA04のモーダルで処理する
    success_url = reverse_lazy('stores:a04_table_management') #編集成功後はA04にリダイレクト
    
    def get_queryset(self): # 編集対象のクエリセットを制限 (現在のユーザーの店舗のテーブルのみ)
        
        # 現在の店舗のテーブルのみ編集可能
        return StoreTable.objects.filter(store=self.request.user.store, deleted_at__isnull=True)
    
    def form_valid(self, form):
        instance = form.save()
        from .utils import generate_qr_code
        generate_qr_code(instance)                # QRコード再生成
        messages.success(self.request, 'テーブル情報を更新しました。QRコードも更新されました。')
        return redirect(self.success_url)
    
class TableDeleteView(LoginRequiredMixin, DeleteView):
    """A04 テーブル削除を処理する (論理削除)"""
    model = StoreTable # 削除対象のモデルはStoreTable
    success_url = reverse_lazy('stores:a04_table_management') # 削除成功後はA04にリダイレクト
    
    # 削除対象のクエリセットを制限 (現在のユーザーの店舗のテーブルのみ)
    def get_queryset(self):
        return StoreTable.objects.filter(
            store=self.request.user.store, # 現在のユーザーの店舗のテーブルのみ削除可能
            deleted_at__isnull=True # まだ削除されていないテーブルのみ
        )
        
    def form_valid(self, form):
        # 論理削除のため、delete()をオーバーライドして、deleted_atに現在の日時を設定
        self.object = self.get_object()
        self.object.deleted_at = timezone.now()
        self.object.save()
        messages.success(self.request, 'テーブルを削除しました。')
        return redirect(self.success_url)
    
    