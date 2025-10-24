from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    """
    Kullanıcıların siteye kayıt olmasını sağlayan, Django'nun hazır araçlarını kullanan
    sınıf tabanlı bir view (görünüm).
    """
    form_class = UserCreationForm
    # Kayıt başarılı olduğunda kullanıcıyı 'login' (giriş yap) sayfasına yönlendirir.
    success_url = reverse_lazy("login")
    # Kayıt formunu göstermek için kullanılacak olan şablon dosyası.
    template_name = "registration/signup.html"