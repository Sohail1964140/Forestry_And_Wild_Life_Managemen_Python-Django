from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'account'


urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name="signUp"),
    path('login/', views.SignInView.as_view(), name="login"),
    path('logout/',views.userLogoutView.as_view(),name='logout'),
    # # passowrd change urls
    path('passwordChange/',views.userPasswordChangeView.as_view(),name='passwordChange'),
    # path('passwordChangeDone/',TemplateView.as_view(template_name='accounts/passwordChangeDone.html'),name='passwordChangeDone'),
    # # password reset urls
]
