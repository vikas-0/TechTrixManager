from django import forms
from .models import *
from eventman.models import *
from django.core.exceptions import ValidationError

class EventRegistrationForm(forms.ModelForm):
    participants = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'data-role':'tagsinput'}),required=True)

    class Meta:
        model=EventRegistration
        fields=['event', 'participants']

    def clean_participants(self):
        try:
            participants_data = self.cleaned_data.get('participants')
            event = self.cleaned_data.get('event')
            participants =[]

            for pd in participants_data.split(','):
                p = Candidate.objects.get(pk=pd)
                participants.append(p)
            if not (event.minParticipant <= len(participants) <= event.maxParticipant):
                raise ValidationError('Number of Participants exceeded')
            return participants
        except Exception:
            raise ValidationError(str(Exception)+'Something wrong with your input. Please try again')

    def __init__(self, *args, **kwargs):
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['event'].empty_label = ''
        # following line needed to refresh widget copy of choice list
        self.fields['event'].widget.choices =self.fields['event'].choices


class GeneralRegistrationForm(forms.ModelForm):

    class Meta:
        model=Candidate
        fields=['name', 'email', 'contactNo', 'college']

    def __init__(self, *args, **kwargs):
        super(GeneralRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['college'].empty_label = ''

class EventParticipationForm(forms.ModelForm):
    class Meta:
        model=EventResult
        fields=['team', 'score', 'participated']

    def clean_participated(self):
        pd=self.cleaned_data.get('participated')
        if not pd:
            raise ValidationError("You need to tick this")
        return pd


    def __init__(self, *args, **kwargs):
        eventId = kwargs.pop('eventId', None)
        super(EventParticipationForm, self).__init__(*args, **kwargs)

        self.fields['team'].empty_label = ''
        self.fields['team'].queryset=EventRegistration.objects.filter(feePaid=True, event=eventId, eventresult__isnull=True )