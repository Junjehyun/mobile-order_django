from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUserManager(BaseUserManager):
    "Emailをユーザー名として使用するカスタムユーザーマネージャー"
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('roles', 'owner') # スーパーユーザーはオーナー役割に設定
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('スーパーユーザーはis_staff=Trueでなければなりません')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('スーパーユーザーはis_superuser=Trueでなければなりません')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    "モバイルオーダーシステム用のログインユーザーモデル"
    username = None # DjangoのAbstractUserモデルのusernameフィールドを削除
    
    #DB定義書と同じく設定
    email = models.EmailField(
        _('メールアドレス'),
        unique=True,
        max_length=120,
        help_text='ログインIDとして使われるメールアドレス'
    )
    name = models.CharField(
        _('名前'),
        max_length=50,
        help_text='ユーザーの名前'
    )
    telephone = models.CharField(
        _('電話番号'),
        max_length=20,
        blank=True,
        null=True,
        help_text='ユーザーの電話番号'
    )
    roles = models.CharField(
        _('役割'),
        max_length=20,
        choices=[
            ('owner', 'オーナー'),
            ('manager', 'マネージャー'),
            ('staff', 'スタッフ'),
        ],
        default='staff',
        help_text='ユーザーの役割'
    )
    
    #Storeモデルとのリレーション
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='店舗',
        help_text='ユーザーが所属する店舗'
    )
    
    
    objects = CustomUserManager()
    
    # ログイン設定
    USERNAME_FIELD = 'email' # ログインに使用するフィールドをemailに設定
    REQUIRED_FIELDS = ['name'] # createsuperuser作成時に必須のフィールドをnameに設定
    
    # Modelのメタ情報
    class Meta:
        verbose_name = 'ユーザー' # 単数形の名前
        verbose_name_plural = 'ユーザー' # 複数形の名前
        ordering = ['email'] # デフォルトの並び順をemailに設定
        
    def __str__(self):
        return self.email
    
    @property
    def get_roles_display(self):
        "テンプレートで {{ request.user.get_roles_display }} を使用可能に"
        role_dict = dict(self.roles.choices)
        return role_dict.get(self.roles, self.roles)
    
    