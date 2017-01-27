from django.conf.urls import url
from . import views

app_name='registration'

urlpatterns = [
    url(r'^$', views.registrationHome, name='home'),
    url(r'^login/', views.loginUser, name='login'),
    url(r'^candidate/', views.verifyCandidate, name='user'),
    url(r'^eventreg/', views.registerForEvent, name='eventreg'),
    url(r'^getFees/(?P<event_id>[0-9]+)', views.getFees, name='getFees')
]