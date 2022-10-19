from django.urls import path
from .views import MinimumWaitingTime, NextClient, Statistics, CounterList, Services, Ticket

app_name = 'demo_queue'
urlpatterns = [
    path('Statistics/', Statistics.as_view()),
    path('Counter/', CounterList.as_view()),
    path('MinimumWaitingTime/<str:service_tag>/', MinimumWaitingTime.as_view()),
    path('NextClient', NextClient.as_view()),
    path('Ticket', Ticket.as_view()),
    path('Services/', Services.as_view()),
]
