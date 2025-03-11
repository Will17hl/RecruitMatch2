from django.db import models

class Vacante(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to ='movie/images/')
    area = models.CharField(blank=True, max_length=250)
    date = models.DateField(blank=True, null=True)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.title)