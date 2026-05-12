from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    name = forms.CharField(
        label="氏名",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500',
            'placeholder': '山田太郎',
        })
    )

    roles = forms.ChoiceField(
        label="役割",
        choices=[
            ('owner', 'オーナー'),
            ('manager', 'マネージャー'),
            ('staff', 'スタッフ'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500',
            'id': 'id_roles'
        })
    )

    store_id = forms.CharField(
        label="店舗ID",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-violet-400',
            'id': 'id_store_id',
            'placeholder': '例: STORE-001'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-purple-500'
        }
        self.fields['email'].widget.attrs.update(common_attrs)
        self.fields['password1'].widget.attrs.update(common_attrs)
        self.fields['password2'].widget.attrs.update(common_attrs)

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data['name']
        user.roles = self.cleaned_data['roles']
        
        if self.cleaned_data.get('store_id'):
            user.store_id = self.cleaned_data['store_id']
        
        user.save()
        return user