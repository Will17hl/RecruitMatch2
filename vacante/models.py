from django.db import models

class Vacante(models.Model):
    nombre_vacante = models.CharField(max_length=100)
    id_vacante = models.IntegerField(unique=True)
    descripcion_vacante = models.TextField()
    ciudad_vacante = models.CharField(max_length=100)
    area_vacante = models.CharField(max_length=100)
    salario_vacante = models.IntegerField()
    empresa_vacante = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='images/', default='images/default_vacante.png')

    def __str__(self):
        return f"Vacante: {self.nombre_vacante} | Ciudad: {self.ciudad_vacante} | Área: {self.area_vacante} | Salario: ${self.salario_vacante} | Empresa: {self.empresa_vacante}"
