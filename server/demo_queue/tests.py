from django.test import TestCase
from .models import *

# Create your tests here.

class ServicesTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="CC", name="Credit Card", estimated_time="245")
        Service.objects.create(tag="A", name="Administration", estimated_time="315")

    def test_get_services(self):
        services_list = Dao.get_services()  
        self.assertEqual(services_list.count(), 2)
        self.assertEqual(services_list[0][0], "Credit Card")
        self.assertEqual(services_list[1][0], "Administration")
        

class NotEmptyQueueTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="A", name="Administration", estimated_time="320")
        service_id = Service.objects.get(name="Administration")
        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=service_id, actual="7", last="12")
        
class QueueTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="CC", name="Credit Card", estimated_time="245")
        Service.objects.create(tag="A", name="Administration", estimated_time="320")
        service = Service.objects.get(name="Administration",)
        Queue.objects.get_or_create(date=date.today().strftime("%Y-%m-%d"), service=service, actual="7", last="12")
        
    def test_get_services(self):
    
        last = Dao.get_a_ticket("Credit Card")
        self.assertEqual(last, 1)
        service_info = Service.objects.get(name="Credit Card")
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 0)
        
        last = Dao.get_a_ticket("Credit Card")
        self.assertEqual(last, 2)
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 0)

        last = Dao.get_a_ticket("Administration")
        self.assertEqual(last, 13)
        service_info = Service.objects.get(name="Administration")
        actual = Queue.objects.get(date=date.today().strftime("%Y-%m-%d"), service=service_info.id).actual
        self.assertEqual(actual, 7)
     
        try:
            Dao.get_a_ticket("Wrong Service")
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
            
class MinWaitTimeTestCase(TestCase):
    def setUp(self):
        Service.objects.create(tag="DM", name="Deposit Money", estimated_time="5")
        Service.objects.create(tag="SP", name="Sending Packages", estimated_time="10")
        sp = Service.objects.get(name="Sending Packages",)
        dm = Service.objects.get(name="Deposit Money",)

        Queue.objects.create(date=date.today().strftime("%Y-%m-%d"), service=dm, actual="0", last="4")

        Counter.objects.create(_id="0", service=dm)
        Counter.objects.create(_id="1", service=dm)
        Counter.objects.create(_id="1", service=sp)

    def test_minimum_waiting_time(self):
        min_wait_time = Dao.minimum_waiting_time("Deposit Money")
        self.assertEqual(5 * ( (8/3) + (1/2)) , min_wait_time)


