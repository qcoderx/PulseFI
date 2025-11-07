from django.urls import path
from .views import SmeRegisterView, LenderRegisterView, LoginView

# This maps to the /auth/ endpoints in the main urls.py
urlpatterns = [
    path('sme/register', SmeRegisterView.as_view(), name='sme-register'),
    path('lender/register', LenderRegisterView.as_view(), name='lender-register'),
    path('login', LoginView.as_view(), name='login'),
]