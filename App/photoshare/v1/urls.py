
from django.urls import path
from .views import *
urlpatterns = [
    path('', upload_page, name='upload_page'),
    path('api/upload', upload_photo_view),
    path('api/presign', presign_key_view, name='presign_api'),
    path('api/logs', send_log, name='logs_api'),

]
