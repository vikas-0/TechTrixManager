from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class EventRegistrationAdmin(admin.ModelAdmin):
    form = EventRegistrationForm

admin.site.register(Candidate)
admin.site.register(EventRegistration, EventRegistrationAdmin)
admin.site.register(EventResult)