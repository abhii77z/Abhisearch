from django.urls import path
from .views import upload_pdf, home  # ✅ now `home` exists

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_pdf, name='upload_pdf'),
]
