from django.conf.urls import url
from . import views

app_name='registration'

urlpatterns = [
    url(r'^$', views.registrationHome, name='home'),
    url(r'^login/', views.loginUser, name='login'),
    url(r'^candidate/', views.verifyCandidate, name='user'),
    url(r'^candidateListinEvent/', views.cadindateDetailsofEvent, name='candidateList'),
    url(r'^eventreg/', views.registerForEvent, name='eventreg'),
    url(r'^generalreg/', views.generalRegistration, name='generalreg'),
    url(r'^logout/', views.logoutUser, name='logout'),
    url(r'^eventregticket/', views.evenregticket, name='evenregticket'),
    url(r'^scoreSub/(?P<event_id>[0-9]+)', views.scoreSub, name='scoreSub')

]