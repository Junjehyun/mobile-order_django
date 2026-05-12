from allauth.account.views import SignupView
from django.shortcuts import render


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