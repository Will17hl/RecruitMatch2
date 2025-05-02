from django.db import models

class Influencer(models.Model):
    nombre_influencer = models.CharField(max_length=100)
    id_influencer = models.IntegerField(unique=True)
    redes_sociales = models.CharField(max_length=255)
    seguidores = models.IntegerField()
    colaboraciones = models.CharField(max_length=255)
    ciudad_influencer = models.CharField(max_length=100)
    area_influencer = models.CharField(max_length=100)
    precio_campaña = models.IntegerField()
    imagen = models.ImageField(upload_to='images/', default='images/default_image.jpg')

    def __str__(self):
        return f"Ciudad: {self.ciudad_influencer}, ID: {self.id_influencer}, Redes: {self.redes_sociales}, Area: {self.area_influencer}, Precio: {self.precio_campaña}, Seguidores: {self.seguidores}"
