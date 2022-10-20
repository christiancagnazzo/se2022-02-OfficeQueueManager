import json

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dao, Counter
from .serializers import CounterSerializer
from time import gmtime
from time import strftime


class Statistics(APIView):
    def get(self, request):
        statistics = Dao().stats()
        return Response(statistics)

# return a list of all the counters
class CounterList(generics.ListCreateAPIView):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer

class MinimumWaitingTime(APIView):
    def get(self, request, service_tag):
        services = Dao().get_services()
        
        for s in services:
            if s[0] == service_tag:
                print("ok")
                return Response(data= {"result" : strftime("%H:%M:%S", gmtime(Dao().minimum_waiting_time(s[1]))) })

        return Response(status = 400, data = "Service Not Found")

class NextClient(APIView):
    def put(self, request):
        data = request.data 

        if "counter_id" not in data:
            return Response(status = 400, data = "Counter Id Requested")

        try:
            next_client = Dao().next_client(data["counter_id"])
        except Exception as e:
            return Response(status = 400, data = str(e))

        return Response(data={'next_client': next_client})
        

class Services(APIView):
    def get(self, request):
        list_of_services = Dao().get_services();

        result = [];

        for s in list_of_services:
            queue = Dao().get_queue(s[1])
            result.append( [s[0], s[1], queue.last, queue.actual]);

        return Response(result)


class Ticket(APIView):
    def put(self, request):
        data = request.data
        
        if "service_name" not in data:
            return Response(status = 400, data = "Service Name Needed")
        
        list_of_services = Dao().get_services()

        for s in list_of_services:
            if s[1] == data["service_name"]:
                return Response(data= {"Ticket" : Dao().get_a_ticket(data["service_name"]), 
                                        "Time": strftime("%H:%M:%S", gmtime(Dao().minimum_waiting_time(data['service_name'])))})

        return Response(status = 400, data = "Service Not Found")

