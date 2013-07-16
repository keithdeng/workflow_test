from django.db import models

# Create your models here.
class DataInput(models.Model):
    title = models.CharField(max_length=200)
    datafile = models.CharField(max_length=200)
    element = models.CharField(max_length=200)
    fit_algorithm = models.CharField(max_length=200)
    pub_data = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title


