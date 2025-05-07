import csv
import os
from django.core.management.base import BaseCommand
from influencer.models import Influencer

class Command(BaseCommand):
    help = 'Importa influencers desde un archivo CSV'

    def handle(self, *args, **kwargs):
        archivo_csv = 'influencers_data.csv'  # Asegúrate de colocar la ruta correcta del archivo CSV
        ruta_absoluta = os.path.join(os.getcwd(), archivo_csv)

        # Verificar si la imagen predeterminada existe
        imagen_predeterminada = os.path.join(os.getcwd(), 'media/images/default_influencer.png')
        
        if not os.path.exists(imagen_predeterminada):
            self.stderr.write(self.style.ERROR("❌ La imagen predeterminada 'default_influencer.png' no se encuentra en la ruta 'media/images/'."))
            return  # Detener la importación si la imagen no existe

        try:
            with open(ruta_absoluta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Crear influencer con la imagen predeterminada
                        Influencer.objects.create(
                            nombre_influencer=row['nombre_influencer'],
                            id_influencer=row['id_influencer'],
                            redes_sociales=row['redes_sociales'],
                            seguidores=int(row['seguidores']),  # Asegúrate de que 'seguidores' sea un número entero
                            colaboraciones=row['colaboraciones'],
                            ciudad_influencer=row['ciudad_influencer'],
                            area_influencer=row['area_influencer'],
                            precio_campaña=float(row['precio_campaña']),
                            imagen='images/default_influencer.png'  # Asignamos la imagen predeterminada
                        )
                    except KeyError as e:
                        self.stderr.write(self.style.ERROR(f"❌ Falta columna: {e}"))
                    except ValueError as e:
                        self.stderr.write(self.style.ERROR(f"❌ Formato inválido en fila: {row} → {e}"))
            self.stdout.write(self.style.SUCCESS('✅ Importación completada correctamente.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ Archivo no encontrado: {ruta_absoluta}"))
