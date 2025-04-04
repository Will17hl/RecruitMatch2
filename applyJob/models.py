from django.db import models

class Applicant(models.Model):
    TYPE_CHOICES = [
        ('influencer', 'Influencer'),
        ('candidato', 'Candidato'),
    ]

    nombre = models.CharField(max_length=100)
    cc = models.CharField(max_length=20, unique=True)
    estudios = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TYPE_CHOICES)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"