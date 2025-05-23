from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
import pandas as pd
import openai
import unicodedata

# Inicializar cliente OpenAI
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Utilidad para normalizar texto (quita tildes, pasa a minúsculas, etc.)
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ''
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.strip().lower()

# Vista principal
from django.http import JsonResponse

def match_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"resultados": []})

    # ✅ Esta línea es clave para que /match/ funcione con GET
    return render(request, "match/match.html")




# Función de matching para empresas
def hacer_match_empresa(vacante, influencers):
    resultados = []
    for i in influencers:
        try:
            seguidores = int(i.get('seguidores', 0))
        except (ValueError, TypeError):
            seguidores = 0

        ciudad_inf = normalizar_texto(i.get('ciudad_influencer', ''))
        area_inf = normalizar_texto(i.get('area_influencer', ''))
        precio_inf = 0
        try:
            precio_inf = float(i.get('precio_campaña', 0))
        except (ValueError, TypeError):
            precio_inf = 0

        # Filtrar estrictamente por precio ±1000
        if vacante['precio_max']:
            rango_inferior = vacante['precio_max'] - 1000
            rango_superior = vacante['precio_max'] + 1000
            if not (rango_inferior <= precio_inf <= rango_superior):
                continue  # descarta influencer fuera del rango de precio

        # Calcular score
        score = 0
        total_criterios = 4

        # Ciudad
        if vacante['ciudad']:
            if ciudad_inf != normalizar_texto(vacante['ciudad']):
                continue  # descartar si no es la ciudad requerida
        else:
            score += 1

        # Área/título
        if vacante['titulo']:
            area_vac = normalizar_texto(vacante['titulo'])
            if not (area_vac in area_inf or area_inf in area_vac):
                continue  # descarta si el área no coincide
        else:
            score += 1

        # Precio dentro del rango, ya validado arriba, sumamos punto
        score += 1

        # Seguidores mínimo (ejemplo 10k)
        if seguidores >= 10000:
            score += 1

        if score == 0:
            continue  # descarta si no cumple ningún criterio

        nombre = i.get('nombre_influencer', 'influencer')
        ciudad = i.get('ciudad_influencer', '')
        area = i.get('area_influencer', '')
        campañas = i.get('colaboraciones', '')

        prompt = (
            f"{nombre} es un/a influencer con {seguidores} seguidores, especializado/a en el área de {area}. "
            f"Actualmente reside en {ciudad} y ha trabajado en campañas como {campañas}. "
            "Redacta una recomendación convincente, profesional y persuasiva para que una empresa lo/la elija para una campaña publicitaria."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
            )
            mensaje = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error en OpenAI: {e}")
            mensaje = f"{nombre} es una excelente opción para tu campaña publicitaria por su número de seguidores y experiencia."

        porcentaje_match = int((score / total_criterios) * 100)

        resultado = {
            'nombre_influencer': nombre,
            'numero_seguidores': seguidores,
            'ciudad_influencer': ciudad,
            'area_influencer': area,
            'colaboraciones': campañas,
            'precio_campaña': precio_inf,
            'mensaje': mensaje,
            'match': porcentaje_match,
        }

        resultados.append(resultado)

    # Ordenar por match (score) y luego por seguidores
    return sorted(resultados, key=lambda x: (x['match'], x['numero_seguidores']), reverse=True)



# Convertir a set de valores normalizados
def convertir_a_set(valor):
    if not valor:
        return set()
    if isinstance(valor, str):
        return set(normalizar_texto(x) for x in valor.split(',') if x.strip())
    elif isinstance(valor, list):
        return set(normalizar_texto(x) for x in valor if isinstance(x, str) and x.strip())
    return set()

# Función de matching para influencers
def hacer_match_influencer(influencer, vacantes):
    # Asegurar que categorias sea lista
    categorias = influencer.get('categorias', [])
    if isinstance(categorias, str):
        categorias = [categorias]
    elif not isinstance(categorias, list):
        categorias = []

    categorias_inf = {normalizar_texto(cat) for cat in categorias if cat.strip()}
    ciudad_inf = normalizar_texto(influencer.get('ciudad', ''))

    try:
        salario_esperado = float(influencer.get('salario_esperado', 0))
        if salario_esperado > 0:
            rango_inferior = salario_esperado - 10000
            rango_superior = salario_esperado + 10000
        else:
            rango_inferior = 0
            rango_superior = float('inf')
    except (ValueError, TypeError):
        rango_inferior = 0
        rango_superior = float('inf')

    resultados = []

    for vac in vacantes:
        area_vacante = normalizar_texto(vac.get('area_vacante', ''))
        categorias_vac = {area_vacante}
        ciudad_vac = normalizar_texto(vac.get('ciudad_vacante', ''))

        if ciudad_inf and ciudad_inf != ciudad_vac:
            continue

        try:
            salario_vac = float(vac.get('salario_vacante', 0))
        except (ValueError, TypeError):
            salario_vac = 0

        if salario_esperado > 0 and not (rango_inferior <= salario_vac <= rango_superior):
            continue

        categorias_match = categorias_inf.intersection(categorias_vac)
        if not categorias_match:
            continue

        coincidencias = 0
        if ciudad_inf and ciudad_inf == ciudad_vac:
            coincidencias += 1
        if categorias_match:
            coincidencias += 1
        coincidencias += 1  # salario ya pasó el filtro

        if coincidencias < 2:
            continue

        total_criterios = 3
        porcentaje_match = int((coincidencias / total_criterios) * 100)

        mensaje = (
            f"Vacante '{vac.get('nombre_vacante', '')}' en {vac.get('ciudad_vacante', '')} que paga {vac.get('salario_vacante', '')}. "
            f"Coincide en categoría(s): {', '.join(categorias_match)}. "
            f"Porcentaje de match: {porcentaje_match}%."
        )

        vac['score'] = porcentaje_match
        vac['mensaje'] = mensaje
        resultados.append(vac)

    # Debug opcional: imprime cuando no se encuentra nada
    if not resultados:
        print("[DEBUG] No se encontraron coincidencias para:")
        print(f" - Categorías INF: {categorias_inf}")
        print(f" - Ciudad INF: {ciudad_inf}")
        print(f" - Rango salarial: {rango_inferior} - {rango_superior}")

    return sorted(resultados, key=lambda x: x['score'], reverse=True)

# API principal para matching
@csrf_exempt
def api_match(request):
    if request.method == 'GET':
        return render(request, 'match/match.html')

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        tipo_usuario = data.get('tipo')
        if not tipo_usuario:
            return JsonResponse({'error': 'Tipo de usuario no especificado'}, status=400)

        try:
            influencers_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'influencers_data.csv'))
            vacantes_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'vacantes_data.csv'))
        except Exception as e:
            return JsonResponse({'error': f'Error al leer archivos CSV: {str(e)}'}, status=500)

        if tipo_usuario == 'empresa':
            try:
                vacante = {
                    'titulo': data.get('titulo', '').strip(),
                    'ciudad': data.get('ciudad', '').strip(),
                    'precio_max': float(data.get('precio_max', 0)),
                }
                influencers = influencers_df.to_dict(orient='records')
                resultados = hacer_match_empresa(vacante, influencers)
                return JsonResponse({'resultados': resultados})
            except Exception as e:
                return JsonResponse({'error': f'Error procesando datos de empresa: {str(e)}'}, status=400)

        elif tipo_usuario == 'influencer':
            try:
                raw_categorias = data.get('categorias', '')
                if isinstance(raw_categorias, str):
                    categorias = [c.strip() for c in raw_categorias.split(',') if c.strip()]
                elif isinstance(raw_categorias, list):
                    categorias = [str(c).strip() for c in raw_categorias if str(c).strip()]
                else:
                    categorias = []
                influencer = {
                    'username': data.get('username'),
                    'categorias': categorias,
                    'ciudad': data.get('ciudad', '').strip(),
                    'salario_esperado': data.get('salario_esperado', 0),
                }
                vacantes = vacantes_df.to_dict(orient='records')
                resultados = hacer_match_influencer(influencer, vacantes)
                return JsonResponse({'resultados': resultados})
            except Exception as e:
                return JsonResponse({'error': f'Error procesando datos del influencer: {str(e)}'}, status=400)

        else:
            return JsonResponse({'error': 'Tipo de usuario inválido'}, status=400)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)