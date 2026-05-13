from django.urls import path
from .views import StoreRegistrationView

app_name = 'stores'

urlpatterns = [
    path('register/', StoreRegistrationView.as_view(), name='a02_store_register'),
]