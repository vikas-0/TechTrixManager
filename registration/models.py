"""
Importing Django libd
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from default.models import College
from eventman.models import Event
from  django.db.models.signals import pre_save

# Create your models here.

GENERAL_REGISTRATION_FEE = 100

class Candidate(models.Model):
    """
    General Registration objects will be stored in this model
    Users with group 'registrar' will be able to register the general Candidates
    """
    name = models.CharField(blank=False, null=False, max_length=50)
    email = models.EmailField(blank=False, null=False)
    contactNo = models.CharField(blank=False, null=False, max_length=10)
    college = models.ForeignKey(College, null=False)
    feePayable = models.IntegerField(default=GENERAL_REGISTRATION_FEE)
    feePaid = models.BooleanField(default=True)
    registeredBy = models.ForeignKey(User, limit_choices_to={'groups__name':'registrar'})
    timeStamp = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name+"-"+str(self.college)


class EventRegistration(models.Model):
    """
    Stores the imformation of event registration
    """
    event = models.ForeignKey(Event, null=False)
    feePayable = models.IntegerField()
    feePaid = models.BooleanField(default=True)
    participants = models.ManyToManyField(Candidate)
    timeStamp = models.DateTimeField(default=timezone.now, editable=False)
    registeredBy = models.ForeignKey(User, limit_choices_to={'groups__name':'registrar'})

    def __str__(self):
        return str(self.event)+" "+str(self.participants.all())

class EventResult(models.Model):
    """
    Model for storing result for events
    """
    team = models.OneToOneField(EventRegistration, null=False)
    participated = models.BooleanField(default=False, null=False)
    score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    status = models.CharField(default='Not participated yet', null=False, max_length=100)
    nextRoundEligibility = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.team.pk)
