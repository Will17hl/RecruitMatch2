from django.db import models

class Vacante(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='vacante/images/', null=True, blank=True, default='vacante/images/default.jpeg')
    company = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(blank=True, max_length=250)
    date = models.DateField(blank=True, null=True)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.title)