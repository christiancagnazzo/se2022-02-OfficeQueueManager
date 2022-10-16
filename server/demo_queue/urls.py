from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import Statistics, CounterList

app_name = 'demo_queue'
urlpatterns = [
    path('Statistics/', Statistics.as_view()),
    path('Counter/', CounterList.as_view()),

]
