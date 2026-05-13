from allauth.account.views import SignupView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy

class CustomSignupView(SignupView):
    """
    A00の新規登録画面
    allauthの基本動作 + メール認証必須 + カスタム成功ページに移動
    """
    def form_valid(self, form):
        # allauthが ユーザーを作成し、確認メールを送信するための基本的な動作を実行
        response = super().form_valid(form)
        
        # メール認証が必要な場合、ユーザーはまだアクティブではないため、ログインさせない
        return render(self.request, 'account/custom_email_sent.html', {
            'email': form.cleaned_data.get('email')
        })
        
    def get_success_url(self):
        """
        - storeがない：A02の店舗登録画面へ
        - storeがある：A03のダッシュボードへ
        """
        user = self.request.user
        if hasattr(user, 'store') and user.store is None:
            return reverse_lazy('stores:a02_store_register') # A02のURLにリダイレクト
        return reverse_lazy('a03_dashboard') # A03のURLにリダイレクト
    
class CustomLoginView(LoginView):
    """
    ログイン有無に応じてリダイレクト先を変更
    store がないユーザーはA02の店舗登録画面へ、
    storeがあるユーザーはA03のダッシュボードへリダイレクト
    """
    template_name = 'admin/A01_login.html'
    redirect_authenticated_user = True # すでにログインしているユーザーはリダイレクトする設定
    
    def get_success_url(self):
        """
        ログイン成功後のリダイレクト先をユーザーのstoreの有無で分岐
        """
        user = self.request.user
        
        # storeがないユーザーはA02の店舗登録画面へリダイレクト
        if hasattr(user, 'store') and user.store is None:
            return reverse_lazy('stores:a02_store_register') # A02のURLにリダイレクト
        
        # storeがあるユーザーはA03のダッシュボードへリダイレクト
        #return reverse_lazy('a03_dashboard') # A03のURLにリダイレクト