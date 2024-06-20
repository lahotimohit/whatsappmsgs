from django.urls import path
from .views import upload_csv, receive_message

urlpatterns = [
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('receive-msg', receive_message)
]
