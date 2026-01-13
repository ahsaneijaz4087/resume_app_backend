from django.urls import path
from .views import signup, login

urlpatterns = [
    path('signup/', signup, name='second-signup'),
    path('login/', login, name='second-login'),
]
