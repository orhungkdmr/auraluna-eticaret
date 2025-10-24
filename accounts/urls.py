from django.urls import path
from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    # Kayıt olma sayfası için URL (örn: /accounts/signup/)
    path("signup/", SignUpView.as_view(), name="signup"),
]