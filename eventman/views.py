from django.http import HttpResponse, JsonResponse
from .models import Event
# Create your views here.

def eventDet(request, event_id):
    try:
        if Event.objects.filter(pk=event_id):
            event=Event.objects.get(pk=event_id)
            return JsonResponse({'resp':True, 'data':{'id': event.pk, 'name': event.name, 'fees':event.fee, 'minParticipant':event.minParticipant, 'maxParticipant': event.maxParticipant, 'maxIsBetter':event.maxIsBetter}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)