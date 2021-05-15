from django.db import models

# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField("",max_length=30)
    email = models.CharField("",max_length=40)
    phone = models.CharField("",max_length=15)
    content = models.CharField("",max_length=2000)
    timestamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name
