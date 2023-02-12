from django.db import models

# Create your models here.
class Task(models.Model):
    name= models.CharField(max_length=120)
    priority = models.CharField(max_length=120)
    date = models.DateField()
    def __str__(self):
        return self.name
