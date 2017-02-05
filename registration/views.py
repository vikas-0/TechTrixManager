from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse
from  ast import literal_eval
from .forms import *
from django.db.models import Sum
from eventman.models import Event as EventList
# Create your views here.

# Home page for candidate registration(General & event)
@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def registrationHome(request):
    return render(request, template_name='base.html')


# Renders login page and also handles login request only for registrar
def loginUser(request):
    redirectTo = ""

    if request.GET:
        redirectTo = request.GET['next']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if 'registrar' in [i.name for i in user.groups.all()]:
                    login(request, user)
                    if redirectTo=="":
                        return render(request, 'base.html')
                    else:
                        # If login page is opened due to failed authentication
                        return HttpResponseRedirect(redirectTo)
                else:
                    return render(request, 'login.html', {'error_message': 'You are not authorised for this section', 'next':redirectTo})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled', 'next':redirectTo})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login', 'next':redirectTo})
    return render(request, template_name='login.html',context={'next':redirectTo})


@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def registerForEvent(request):
    form = EventRegistrationForm(request.POST or None)

    # Calculate money by the user
    # moneyEarned =0
    moneyEarnedbyEvent=EventRegistration.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyEvent=moneyEarnedbyEvent if moneyEarnedbyEvent is not None else 0
    moneyEarnedbyGen=Candidate.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyGen = moneyEarnedbyGen if moneyEarnedbyGen is not None else 0
    moneyEarned=moneyEarnedbyEvent+moneyEarnedbyGen
    moneyEarned=moneyEarned if moneyEarned is not None else 0

    if form.is_valid():
        registration =form.save(commit=False)
        registration.registeredBy = request.user
        registration.feePayable = registration.event.fee
        registration.save()
        form.save_m2m()

        contexts = {'user': request.user.username, 'money': moneyEarned, 'registratinid':registration.pk, 'registeredevent':registration.event.name, 'regfee': registration.feePayable, 'backurl':reverse('registration:eventreg')}
        messages.add_message(request,messages.INFO,contexts)
        return HttpResponseRedirect(reverse('registration:evenregticket'))
        # return render(request, template_name='eventregtikcet.html', context=contexts)
    contexts = {'form': form, 'user': request.user.username, 'money': moneyEarned}
    return render(request, template_name='eventreg.html',context=contexts)


@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def generalRegistration(request):
    form = GeneralRegistrationForm(request.POST or None)

    # Calculate money by the user
    # moneyEarned =0
    moneyEarnedbyEvent=EventRegistration.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyEvent=moneyEarnedbyEvent if moneyEarnedbyEvent is not None else 0
    moneyEarnedbyGen=Candidate.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyGen = moneyEarnedbyGen if moneyEarnedbyGen is not None else 0
    moneyEarned=moneyEarnedbyEvent+moneyEarnedbyGen

    #Check form data
    if form.is_valid():
        registration =form.save(commit=False)
        registration.registeredBy = request.user
        registration.save()
        contexts = {'user': request.user.username, 'money': moneyEarned, 'registratinid':registration.pk, 'registeredevent':"General Registration", 'regfee': registration.feePayable, 'backurl': reverse('registration:generalreg')}
        messages.add_message(request,messages.INFO,contexts)
        return HttpResponseRedirect(reverse('registration:evenregticket'))
        # return render(request, template_name='eventregtikcet.html', context=contexts)
    contexts = {'form': form, 'user': request.user.username, 'money': moneyEarned, 'fee':GENERAL_REGISTRATION_FEE}
    return render(request, template_name='generalreg.html',context=contexts)

# Score submission view
@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'coordinator' in [i.name for i in user.groups.all()])
def scoreSub(request, event_id):
    event=get_object_or_404(EventList, pk=event_id)
    eventName=event.name
    form = EventParticipationForm(request.POST or None, eventId=event)

    #Check form data
    if form.is_valid():
        result =form.save(commit=False)
        result.scoreSubmittedBy = request.user
        result.save()
        return render(request, template_name='scoresubmisiion.html', context={'form':form,'eventName':eventName,'user':request.user.username,'event':event_id, 'message':'Score Recorded, Submit Another'})
    contexts = {'form': form, 'eventName':eventName,'user': request.user.username, 'event':event_id}
    return render(request, template_name='scoresubmisiion.html',context=contexts)

@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'coordinator' in [i.name for i in user.groups.all()])
def leaderBoard(request, event_id):
    event=get_object_or_404(EventList, pk=event_id)
    eventName=event.name
    resultset=EventResult.objects.filter(team__event=event)
    table=LeaderBoardTable(resultset)
    contexts = {'eventName':eventName,'user': request.user.username,'event':event_id, 'table':table }
    return render(request, template_name='leaderboard.html',context=contexts)


@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def evenregticket(request):
    storage=messages.get_messages(request)
    contexts=None
    for message in storage:
        contexts=message
        break
    jsonstring=str(contexts)
    contexts=literal_eval(jsonstring)
    # return HttpResponse(context)
    return render(request, template_name='eventregtikcet.html', context=contexts)


# APIs ....
''''''
def verifyCandidate(request):
    """
    Returns candidate details
    :param request:
    :return: boolean
    """
    try:
        if request.method=='GET':
            id=request.GET.copy()
            if 'id' in id :
                userid = id['id']
                if Candidate.objects.filter(pk=userid):
                    candidate=Candidate.objects.get(pk=userid)
                    return JsonResponse({'resp':True, 'data':{'id': candidate.pk, 'name': candidate.name, 'college':candidate.college.name}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)


def cadindateDetailsofEvent(request):
    """
    Returns candidate details
    :param request:
    :return: boolean
    """
    try:
        if request.method=='GET':
            id=request.GET.copy()
            if 'id' in id :
                eventRegistrationId = id['id']
                if EventRegistration.objects.filter(pk=eventRegistrationId):

                    eventRegistration=EventRegistration.objects.get(pk=eventRegistrationId)
                    htmlTable=''
                    print((eventRegistration.participants.all()))
                    for candidate in eventRegistration.participants.all():

                        htmlTable=htmlTable+'<tr><td>'+str(candidate.name)+'</td><td>'+str(candidate.college)+'</td></tr>'
                    return JsonResponse({'resp':True, 'data':{'id': candidate.pk, 'table': htmlTable}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)




def logoutUser(request):
    logout(request)
    return render(request, 'login.html', {'error_message': 'Logged Out', 'next': request})