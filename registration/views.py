from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import Candidate
from .forms import *
from django.db.models import Sum


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
    moneyEarned=EventRegistration.objects.filter(registeredBy=request.user).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarned=moneyEarned if moneyEarned is not None else 0
    if form.is_valid():
        registration =form.save(commit=False)
        registration.registeredBy = request.user
        registration.feePayable = registration.event.fee
        registration.save()
        return HttpResponse(str(registration.pk))
    contexts = {'form': form, 'user': request.user.first_name + ' ' + request.user.last_name, 'money': moneyEarned}
    return render(request, template_name='eventreg.html',context=contexts)


# APIs ....

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

def getFees(request, event_id):
    return HttpResponse(event_id)