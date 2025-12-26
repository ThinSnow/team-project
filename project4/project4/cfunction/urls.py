from django.urls import path
from cfunction import sign_in_out

urlpatterns = [
    path('login',sign_in_out.dispatcher),
]