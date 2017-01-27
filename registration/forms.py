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

            if event.minParticipant <= len(participants) <= event.maxParticipant:
               pass
            else:
                raise ValidationError('Number of Participants should be in between '+str(event.minParticipant)+' and '+str(event.maxParticipant))

            return participants
        except Exception:
            raise ValidationError(str(Exception)+'Something wrong with your input. Please try again')

    def __init__(self, *args, **kwargs):
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['event'].empty_label = ''
        # following line needed to refresh widget copy of choice list
        self.fields['event'].widget.choices =self.fields['event'].choices
