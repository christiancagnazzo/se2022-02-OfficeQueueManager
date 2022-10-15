from msilib.schema import Error
from django.db import models
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

# Create your models here.

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length = 5)
    name = models.CharField(max_length = 30)
    estimated_time = models.IntegerField()  

    def __str__(self) -> str:
        return f"{self.id}, {self.tag}, {self.name}, {self.estimated_time}"

class Counter(models.Model):
    _id = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['id', 'service'],
            name='unique_1'
        )]
    
    def __str__(self) -> str:
        return f"{self._id}, {self.service}"

class Queue(models.Model):
    date = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    actual = models.IntegerField()
    last = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['date', 'service'],
            name='unique_2'
        )]
    
    def __str__(self) -> str:
        return f"{self.date}, {self.service}, {self.actual}, {self.last}"

class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    salt = models.CharField(max_length=256)
    role = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.username}, {self.password}, {self.salt}, {self.role}"

class Dao():
    def get_services():
        #returns <QuerySet [('Shipping',), ('Account Management',), ('Credit Card',), ('Pension',)]>
        return Service.objects.values_list('name')
    
    

    def minimum_waiting_time(service_name):
        try:
            service_info = Service.objects.get(name=service_name)
        except ObjectDoesNotExist:
            raise Error
        today = date.today().strftime("%Y-%m-%d")
        queue = Queue.objects.get(service = service_info.id, date=today)
        n_r = queue.last - queue.actual
        t_r = service_info.estimated_time
        counters = Counter.objects.filter(service_id=service_info.id).annotate(num_services=Count('_id'))
        sum = 0
        for c in counters:
            sum += float(1/c.num_services)
        
        return t_r * (( n_r / sum) + 1/2)

    def next_client(counter_id):
        services_list = Counter.objects.filter(_id=counter_id).values_list('service_id', flat=True)
        today = date.today().strftime("%Y-%m-%d")
        queues = Queue.objects.filter(service__in = services_list, date=today)
        if len(queues) == 0:
            return -1
        max_length = -1
        for q in queues:
            if q.last - q.actual > max_length:
                max_length = q.last - q.actual
        if max_length < 1:
            return -1
        candidate_queues = []
        for q in queues:
            if q.last - q.actual == max_length:
                candidate_queues.append(q)
        if len(candidate_queues) == 0:
            return -1

        if len(candidate_queues) == 1:
            candidate_queues[0].actual += 1
            candidate_queues[0].save()
            return candidate_queues[0].service.tag + str(candidate_queues[0].actual)
        else:
            min_service_time = -1
            
            pos = -1
            for idx, q in enumerate(candidate_queues):
                ser = q.service
                if min_service_time > ser.estimated_time:
                    min_service_time = ser.estimated_time
                    pos = idx
                    
            candidate_queues[pos].actual += 1
            candidate_queues[pos].save()
            return candidate_queues[pos].service.tag + str(q.actual)
            
                
            


    def get_a_ticket(service_name):
        
        service_id = None
        try:
            service_id = Service.objects.get(name=service_name,)
        except ObjectDoesNotExist:
            raise Error
        today = date.today().strftime("%Y-%m-%d")
        queue, _ = Queue.objects.get_or_create(
            date=today,
            service = service_id, 
            defaults={'actual': 0, 'last': 0})
        queue.last += 1
        queue.save(force_update=True)
        return queue.last


            

