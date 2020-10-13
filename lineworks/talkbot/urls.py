from django.urls import path
from .views import * 
from .models import *

app_name = 'talkbot'

urlpatterns = [
    path('callback/', SendMessage.as_view(), name='send-message'),
    ]