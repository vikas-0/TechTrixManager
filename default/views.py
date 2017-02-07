from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from chartit import DataPool, Chart
from registration.models import *
from django.db.models import Sum, Count
# Create your views here.

@user_passes_test(lambda u: u.is_superuser, login_url='/reg/login/')
def statistics(request):

    moneyByGenralReg=Candidate.objects.aggregate(Sum('feePayable'))['feePayable__sum']
    moneyByEventReg=EventRegistration.objects.aggregate(Sum('feePayable'))['feePayable__sum']
    totalMoney=moneyByEventReg+moneyByGenralReg

    # print (EventRegistration.objects.values('registeredBy__username').annotate(money=Sum('feePayable')))
    # print(Candidate.objects.values('registeredBy__username').annotate(money=Sum('feePayable')))
    ds=DataPool(
        series=[
            {'options':{
                'source':EventRegistration.objects.values('event').annotate(fee=Sum('feePayable'), count=Count('event'))
            },
                'terms':['event',
                         'fee',
                         'count']

            }
        ]
    )

    ds1=DataPool(
        series=[
            {
                'options':{
                    'source':EventRegistration.objects.values('registeredBy__username').annotate(money=Sum('feePayable'))
                },
                'terms':['registeredBy__username',
                         'money']
            },
            # {
            #     'options': {
            #         'source': Candidate.objects.values('registeredBy__username').annotate(money=Sum('feePayable'))
            #     },
            #     'terms': ['registeredBy__username',
            #               'money']
            # }
        ]
    )

    cht0= Chart(
        datasource=ds1,
        series_options=[{'options': {
            'type': 'column',
            'stacking': True},
            'terms': {
                'registeredBy__username': [
                    'money'],

            }}],
        chart_options={'title': {
            'text': 'Event Registration'},
            'xAxis': {
                'title': {
                    'text': 'Member'}}}
    )

    def EventName(id):
        return Event.objects.get(pk=id).name


    cht= Chart(
        datasource=ds,
        series_options=[
            {
                'options':{
                    'type':'pie',
                    'stacking':False},
                'terms':{
                    'event':[
                        'fee'
                    ]
                }
            }
        ],
        chart_options=
        {'title': {
            'text': 'Event BreakDown By Money'},
            'xAxis': {
                'title': {
                    'text': 'Event'}}},
        x_sortf_mapf_mts=(None, EventName, False )

    )

    cht2= Chart(
        datasource=ds,
        series_options=[
            {
                'options':{
                    'type':'pie',
                    'stacking':False},
                'terms':{
                    'event':[
                        'count'
                    ]
                }
            }
        ],
        chart_options=
        {'title': {
            'text': 'Event BreakDown By Number of Teams Participated'},
            'xAxis': {
                'title': {
                    'text': 'Event'}}},
        x_sortf_mapf_mts=(None, EventName, False )

    )

    return render_to_response('charts.html', {'charts':[cht0,cht,cht2],'genregmoney':moneyByGenralReg, 'eventregmoney':moneyByEventReg, 'totalmoney':totalMoney})