from django.db import models

# Create your models here.

# wanted to type SITL but mistyped it as STIL
class STIL_Report(models.Model):
    start_datetime_field = models.DateTimeField('start_date')
    end_datetime_field = models.DateTimeField('end_date')
    fom = models.IntegerField()
    id_record = models.CharField(max_length=100)
    # apologies for misspelling discussion
    discusson = models.CharField(max_length=400)

    def __str__(self):
        return '{}--{}--{}'.format(self.start_datetime_field, self.fom, self.discusson)