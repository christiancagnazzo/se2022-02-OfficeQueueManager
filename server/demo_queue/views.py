import json

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dao, Counter
from .serializers import CounterSerializer


class Statistics(APIView):

    def get(self, request):
        statistics = Dao().stats()
        return Response(statistics)

# return a list of all the counters
class CounterList(generics.ListCreateAPIView):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer



