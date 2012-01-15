from django.db import models
from synclee.work.models import Work
from synclee.club.models import Catalog
# Create your models here.

class Recommand(models.Model):
    feature = models.IntegerField(null=True)
    fea_fiction = models.IntegerField(null=True)
    fea_illust = models.IntegerField(null=True)
    fea_comic = models.IntegerField(null=True)
    rec = models.CharField(max_length=50, null=True)
    rec_fiction = models.CharField(max_length=50, null=True)
    rec_illust = models.CharField(max_length=50, null=True)
    rec_comic = models.CharField(max_length=50, null=True)
    
    def get_recommand(self, cata_name):
        if cata_name == 'fiction':
            work_id = self.rec_fiction.split(',')
        elif cata_name == 'illust':
            work_id = self.rec_illust.split(',')
        elif cata_name == 'comic':
            work_id = self.rec_comic.split(',')
        else:
            id_str = str(self.rec)
            work_id = id_str.split(',')
        id_list = []
        for w in work_id:
            if w != "":
                id_list.append(int(w))
        works = Work.objects.filter(id__in=id_list)
        return works
    
    def get_feature(self, cata_name):
        if cata_name == 'fiction':
            work_id = self.fea_fiction
        elif cata_name == 'illust':
            work_id = self.fea_illust
        elif cata_name == 'comic':
            work_id = self.fea_comic
        else:
            work_id = self.feature
        try:
            work = Work.objects.get(pk=work_id)
        except:
            work = None
        return work