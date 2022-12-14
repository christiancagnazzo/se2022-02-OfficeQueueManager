import json
from symbol import factor
from django.test import RequestFactory, TestCase
from .models import *
from rest_framework.test import APITestCase

# Create your tests here.

# UNIT TEST

class ServicesTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="CC", name="Credit Card", estimated_time="245")
        Service.objects.create(tag="A", name="Administration", estimated_time="315")

    def test_get_services(self):
        services_list = Dao().get_services()  
        self.assertEqual(services_list.count(), 2)
        self.assertEqual(services_list[0][0], "A")
        self.assertEqual(services_list[0][1], "Administration")
        self.assertEqual(services_list[1][0], "CC")
        self.assertEqual(services_list[1][1], "Credit Card")
        

class NotEmptyQueueTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="A", name="Administration", estimated_time="320")
        service_id = Service.objects.get(name="Administration")
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=service_id, actual="7", last="12")


class QueueTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="CC", name="Credit Card", estimated_time="245")
        Service.objects.create(tag="A", name="Administration", estimated_time="320")
        service = Service.objects.get(name="Administration", )
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=service, actual="7", last="12")

    def test_get_services(self):

        last = Dao().get_a_ticket("Credit Card")
        self.assertEqual(last, "CC" + str(1))
        service_info = Service.objects.get(name="Credit Card")
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 0)

        last = Dao().get_a_ticket("Credit Card")
        self.assertEqual(last, "CC" + str(2))
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 0)

        last = Dao().get_a_ticket("Administration")
        self.assertEqual(last, "A" + str(13))
        service_info = Service.objects.get(name="Administration")
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 7)

        try:
            Dao().get_a_ticket("Wrong Service")
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


class MinWaitTimeTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="5")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="10")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="0", last="4")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_minimum_waiting_time(self):
        min_wait_time = Dao().minimum_waiting_time("Deposit Money")
        self.assertEqual(5 * ( (8/3) + (1/2)) , min_wait_time)


class NextClientDifferentQueueLengthTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="5")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="10")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="5", last="12")
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=sp, actual="3", last="7")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_next_client(self):
        next_client = Dao().next_client(1)
        self.assertEqual("DM" + str(6), next_client)


class NextClientSameQueueLengthTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="10")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="5")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="5", last="12")
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=sp, actual="10", last="17")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_next_client(self):
        next_client = Dao().next_client(1)
        self.assertEqual("SP" + str(11), next_client)


class CompletedWorkFlowTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="10")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="5")

        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)
       

    def test_next_client(self):
        last = Dao().get_a_ticket("Deposit Money")
        self.assertEqual(last, "DM" + str(1))

        last = Dao().get_a_ticket("Deposit Money")
        self.assertEqual(last, "DM" + str(2))

        last = Dao().get_a_ticket("Sending Packages")
        self.assertEqual(last, "SP" + str(1))

        last = Dao().get_a_ticket("Deposit Money")
        self.assertEqual(last, "DM" + str(3))

        last = Dao().get_a_ticket("Sending Packages")
        self.assertEqual(last, "SP" + str(2))

        next_client = Dao().next_client(1)
        self.assertEqual(next_client, "DM" + str(1))

        next_client = Dao().next_client(0)
        self.assertEqual(next_client, "DM" + str(2))

        next_client = Dao().next_client(1)
        self.assertEqual(next_client, "SP" + str(1))

        next_client = Dao().next_client(0)
        self.assertEqual(next_client, "DM" + str(3))

        next_client = Dao().next_client(1)
        self.assertEqual(next_client, "SP" + str(2))

"""
class StatsTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="10")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="5")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        # Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="4", last="4")
        # Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=sp, actual="12", last="12")
        # Queue.objects.create(date=date.weekday().strftime("%Y-%m-%d"), service=dm, actual="11", last="11")
        # Queue.objects.create(date="2022-10-15", service=sp, actual="7", last="7")
        # Queue.objects.create(date="2022-10-01", service=dm, actual="6", last="6")
        # Queue.objects.create(date="2022-10-02", service=sp, actual="10", last="10")
        # Queue.objects.create(date="2022-09-16", service=dm, actual="2", last="2")
        # Queue.objects.create(date="2022-09-16", service=sp, actual="20", last="20")

    def test_stats(self):
        stats = Dao.stats()
        
        self.assertEqual(stats["daily"]["Deposit Money"], 4)
        self.assertEqual(stats["daily"]["Sending Packages"], 12)
        self.assertEqual(stats["weekly"]["Deposit Money"], 15)
        self.assertEqual(stats["weekly"]["Sending Packages"], 19)
        self.assertEqual(stats["monthly"]["Deposit Money"], 21)
        self.assertEqual(stats["monthly"]["Sending Packages"], 29)    
"""

# INTEGRATION TEST

class MinWaitTimeTestCaseAPITest(APITestCase): 
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="5")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="10")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="0", last="4")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_min_wait_time_api(self):
        response = self.client.get('/demo/MinimumWaitingTime/DM', format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'result': 5 * ( (8/3) + (1/2))})


class NextClientAPITest(APITestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="5")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="10")
        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="5", last="12")
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=sp, actual="3", last="7")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_next_client_api(self):
        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'DM6'})


class CompletedWorkFlowAPITestCase(APITestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="10")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="5")

        sp = Service.objects.get(name="Sending Packages", )
        dm = Service.objects.get(name="Deposit Money", )

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_workflow_api(self):
        response = self.client.put('/demo/Ticket', format='json', data={"service_name": "Deposit Money"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Ticket'], "DM1")

        response = self.client.put('/demo/Ticket', format='json', data={"service_name": "Deposit Money"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Ticket'], "DM2")

        response = self.client.put('/demo/Ticket', format='json', data={"service_name": "Sending Packages"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Ticket'], "SP1")
       
        response = self.client.put('/demo/Ticket', format='json', data={"service_name": "Deposit Money"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Ticket'], "DM3")

        response = self.client.put('/demo/Ticket', format='json', data={"service_name": "Sending Packages"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Ticket'], "SP2")
        
        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'DM1'})

        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 0}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'DM2'})

        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'SP1'})

        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 0}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'DM3'})

        response = self.client.put('/demo/NextClient', format='json', data={"counter_id": 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'next_client': 'SP2'})