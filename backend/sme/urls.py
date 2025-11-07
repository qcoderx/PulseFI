from django.urls import path
from .views import (
    BusinessProfileView, 
    CACUploadView, 
    VideoUploadView, 
    MonoConnectView,
    SMEBashboardView
)

# This maps to the /sme/ endpoints in the main urls.py
urlpatterns = [
    path('profile', BusinessProfileView.as_view(), name='sme-profile'),
    path('upload/cac', CACUploadView.as_view(), name='sme-upload-cac'),
    path('upload/video', VideoUploadView.as_view(), name='sme-upload-video'),
    path('mono/connect', MonoConnectView.as_view(), name='sme-mono-connect'),
    path('dashboard', SMEBashboardView.as_view(), name='sme-dashboard'),
]