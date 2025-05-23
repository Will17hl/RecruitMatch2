from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from django.conf import settings
import os
import openai

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def hacer_match_empresa(vacante, influencers):
    resultados = []
    for i in influencers:
        # Filtrar ciudad (usa campo correcto de CSV: ciudad_influencer)
        if vacante['ciudad'] and i.get('ciudad_influencer', '').lower() != vacante['ciudad'].lower():
            continue
        # Filtrar precio (usa campo correcto: precio_campaña)
        if vacante['precio_max'] and float(i.get('precio_campaña', 0)) > vacante['precio_max']:
            continue
        score = 0
        if int(i.get('seguidores', 0)) > 10000:
            score += 10
        if score > 0:
            i['score'] = score
            resultados.append(i)
    return sorted(resultados, key=lambda x: x['score'], reverse=True)

def hacer_match_influencer(influencer, vacantes):
    resultados = []
    for v in vacantes:
        score = 0
        if influencer['redes_sociales']:
            redes_en_comun = set(influencer['redes_sociales']) & set(v.get('redes_sociales', []))
            score += len(redes_en_comun) * 20
        if v['ciudad'] and influencer['ciudad'] and v['ciudad'].lower() == influencer['ciudad'].lower():
            score += 10
        if float(v.get('salario', 0)) <= float(influencer.get('salario_esperado', 0)):
            score += 10
        if score > 0:
            v['score'] = score
            resultados.append(v)
    return sorted(resultados, key=lambda x: x['score'], reverse=True)

@csrf_exempt
def api_match(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo')

            base_path = settings.BASE_DIR

            if tipo == 'empresa':
                vacante = {
                    'titulo': data.get('titulo'),
                    'ciudad': data.get('ciudad', '').strip(),
                    'precio_max': float(data.get('precio_max', 0)),
                }
                influencers = pd.read_csv(os.path.join(base_path, 'influencers_data.csv')).to_dict('records')
                resultados = hacer_match_empresa(vacante, influencers)

                for i in resultados[:5]:
                    # Usa nombre_influencer para mostrar en frontend y en prompt
                    nombre = i.get('nombre_influencer', 'Influencer')
                    prompt = f"Escribe un mensaje corto para que el influencer {nombre} se interese en la vacante '{vacante['titulo']}' ubicada en {vacante['ciudad']}."
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=30,
                    )
                    i['mensaje'] = response.choices[0].message.content.strip()
                    i['nombre_influencer'] = nombre  # asegúrate que venga en la respuesta

                return JsonResponse({'resultados': resultados})

            elif tipo == 'influencer':
                influencer = {
                    'username': data.get('username'),
                    'redes_sociales': data.get('redes_sociales', []),
                    'ciudad': data.get('ciudad', '').strip(),
                    'salario_esperado': float(data.get('salario_esperado', 0)),
                }
                vacantes = pd.read_csv(os.path.join(base_path, 'vacantes_data.csv')).to_dict('records')
                resultados = hacer_match_influencer(influencer, vacantes)

                for v in resultados[:5]:
                    prompt = f"Escribe un mensaje para el influencer {influencer['username']} recomendándole la vacante '{v['titulo']}' que paga hasta {v.get('salario', 'N/A')}."
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=30,
                    )
                    v['mensaje'] = response.choices[0].message.content.strip()

                return JsonResponse({'resultados': resultados})

            else:
                return JsonResponse({'error': 'Tipo no válido'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
