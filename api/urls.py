from django.urls import path

from . import views
from .views import QrView

urlpatterns = [
    path('', QrView.as_view(), name='home'),
    path('create-tx/', views.create_tx, name='create-tx'),
    path('get-tx/<pk>', views.get_tx, name='get-tx'),
    path('generate-qrcode/', views.generate_qrcode, name='generate-qrcode'),
]
