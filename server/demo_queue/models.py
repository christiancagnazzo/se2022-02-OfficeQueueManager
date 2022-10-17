from enum import unique
from django.db import models
from django.db.models import Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from datetime import date


# Create your models here.

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=5)
    name = models.CharField(max_length=30)
    estimated_time = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'tag'],
            name='unique_0'
        )]

    def __str__(self) -> str:
        return f"{self.id}, {self.tag}, {self.name}, {self.estimated_time}"


class Counter(models.Model):
    _id = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['_id', 'service'],
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


class Dao:
    def get_services(self):
        # returns <QuerySet [('Shipping',), ('Account Management',), ('Credit Card',), ('Pension',)]>
        return Service.objects.values_list('name')

    def minimum_waiting_time(self, service_name):
        try:
            service_info = Service.objects.get(name=service_name)
        except ObjectDoesNotExist:
            raise Exception()
        today = date.today().strftime("%Y-%m-%d")
        queue = Queue.objects.get(service=service_info.id, date=today)
        n_r = queue.last - queue.actual
        t_r = service_info.estimated_time
        counters_id = Counter.objects.filter(service=service_info.id).values_list('_id')
        counters = Counter.objects.values('_id').annotate(num_services=Count('_id')).filter(_id__in=counters_id)
        k_i = [1,2]
        s_i_r = [1,1]
        sum_k = sum(map(lambda i,j:1/i * j ,k_i,s_i_r))
        if sum_k == 0:
            return "No service center provide service"
        #print("sun_k:"+str(sum_k))
        T_r = t_r * (n_r/sum_k + 0.5)
        #this kind of algorithom will cause bug:because of deviation, it gives 15:49 and the current answer is 15:50
        #hour = int(time)
        #minute = int((time - hour)*60 )
        hour = int(T_r * 60 //60)
        minute = int(round(T_r * 60 % 60,0))
        if minute<10:
            minute = "0"+str(minute)
        else:
            minute = str(minute)
        #print("" + str(hour) +":" + minute)
        return "" + str(hour) +":" + minute

    def next_client(counter_id):
        services_list = Counter.objects.filter(_id=counter_id).values_list('service_id', flat=True)
        today = date.today().strftime("%Y-%m-%d")
        queues = Queue.objects.filter(service__in=services_list, date=today)
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
            return candidate_queues[pos].service.tag + str(candidate_queues[pos].actual)

    def get_a_ticket(service_name):

        service_id = None
        try:
            service_id = Service.objects.get(name=service_name, )
        except ObjectDoesNotExist:
            raise Exception()
        today = date.today().strftime("%Y-%m-%d")
        queue, _ = Queue.objects.get_or_create(
            date=today,
            service=service_id,
            defaults={'actual': 0, 'last': 0})
        queue.last += 1
        queue.save()
        return queue.service.tag + str(queue.last)

    def stats():
        this_month = date.today().strftime("%m")
        this_isoweek = int(date.today().strftime("%V"))
        today = date.today().strftime("%Y-%m-%d")
        monthly_data = Queue.objects.filter(date__month=this_month)
        stats = {
            'daily': {},
            'weekly': {},
            'monthly': {}
        }
        for ser in Service.objects.values_list('name', flat=True):
            for x in stats:
                stats[x][ser] = 0

        for q in monthly_data.filter(date=today):
            stats['daily'][q.service.name] = q.actual

        for q in monthly_data.filter(date__week=this_isoweek).values('service__name').annotate(tot=Sum('actual')):
            stats['weekly'][q['service__name']] = q['tot']

        for q in monthly_data.values('service__name').annotate(tot=Sum('actual')):
            stats['monthly'][q['service__name']] = q['tot']

        return stats
