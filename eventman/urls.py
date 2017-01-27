from django.conf.urls import url
from . import views

app_name='registration'

urlpatterns = [
    url(r'^$', views.registrationHome, name='home'),
    url(r'^login/', views.loginUser, name='login'),
    url(r'^candidate/', views.verifyCandidate, name='user')
]