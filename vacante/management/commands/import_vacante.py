import csv
import os
from django.core.management.base import BaseCommand
from vacante.models import Vacante  # Asegúrate de importar el modelo Vacante

class Command(BaseCommand):
    help = 'Importa vacantes desde un archivo CSV'

    def handle(self, *args, **kwargs):
        archivo_csv = 'vacantes_data.csv'  # Asegúrate de colocar la ruta correcta del archivo CSV
        ruta_absoluta = os.path.join(os.getcwd(), archivo_csv)

        # Verificar si la imagen predeterminada existe
        imagen_predeterminada = os.path.join(os.getcwd(), 'media/images/default_vacante.png')
        
        if not os.path.exists(imagen_predeterminada):
            self.stderr.write(self.style.ERROR("❌ La imagen predeterminada 'default_vacante.png' no se encuentra en la ruta 'media/images/'."))  
            return  # Detener la importación si la imagen no existe

        try:
            with open(ruta_absoluta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Crear vacante con la imagen predeterminada
                        Vacante.objects.create(
                            nombre_vacante=row['nombre_vacante'],
                            id_vacante=row['id_vacante'],
                            descripcion_vacante=row['descripcion_vacante'],
                            ciudad_vacante=row['ciudad_vacante'],
                            area_vacante=row['area_vacante'],
                            salario_vacante=float(row['salario_vacante']),  # Asegúrate de que 'salario_vacante' sea un número flotante
                            empresa_vacante=row['empresa_vacante'],
                            imagen='images/default_vacante.png'  # Asignamos la imagen predeterminada
                        )
                    except KeyError as e:
                        self.stderr.write(self.style.ERROR(f"❌ Falta columna: {e}"))
                    except ValueError as e:
                        self.stderr.write(self.style.ERROR(f"❌ Formato inválido en fila: {row} → {e}"))
            self.stdout.write(self.style.SUCCESS('✅ Importación completada correctamente.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ Archivo no encontrado: {ruta_absoluta}"))
