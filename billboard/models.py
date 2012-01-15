from django.db import models
from synclee.work.models import Work
from synclee.club.models import Catalog
# Create your models here.

class Board(models.Model):
    order = models.CharField(max_length=1000, null=True)
    order_fiction = models.CharField(max_length=1000, null=True)
    order_illust = models.CharField(max_length=1000, null=True)
    order_comic = models.CharField(max_length=1000, null=True)
    
    def get_board(self, cata_name):
        
        if cata_name == 'fiction':
            work_id = self.order_fiction.split(',')
        elif cata_name == 'illust':
            work_id = self.order_illust.split(',')
        elif cata_name == 'comic':
            work_id = self.order_comic.split(',')
        else:
            work_id = self.order.split(',')
        id_list = []
        for i in range(len(work_id)):
            if work_id[i] != "":
                id_list.append(int(work_id[i]))
        works = []
        for d in id_list:
            works.append(Work.objects.get(pk=d))
        return works