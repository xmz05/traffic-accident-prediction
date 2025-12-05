import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

from .models import PredictionLog
from .ml.model import predict_probability


def _classify_cause(hour, traffic_density, is_bad_weather):
    if is_bad_weather and traffic_density > 0.4:
        return "Плохая погода и высокая плотность движения"
    if is_bad_weather:
        return "Неблагоприятные погодные условия"
    if traffic_density > 0.7 and (7 <= hour <= 10 or 17 <= hour <= 20):
        return "Плотный поток в часы пик"
    if traffic_density > 0.7:
        return "Высокая плотность транспортного потока"
    return "Смешанные факторы (человеческий фактор, дорожные условия)"

def _classify_jam(prob, traffic_density):
    score = prob * 0.7 + traffic_density * 0.3
    if score < 0.2:
        return "нет затора", "Серьезного влияния на трафик не ожидается."
    elif score < 0.5:
        return "локальный затор", "Возможны кратковременные локальные затруднения движения."
    elif score < 0.8:
        return "существенный затор", "Вероятно замедление движения на нескольких прилегающих участках."
    else:
        return "сильный затор", "Высокий риск значительного затора и роста времени в пути."

@csrf_exempt
def predict_accident(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    road_segment = data.get("road_segment")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    dt_str = data.get("datetime")
    weather = data.get("weather", "clear")
    traffic_density = float(data.get("traffic_density", 0.5))

    if dt_str:
        dt = parse_datetime(dt_str)
        if dt is None:
            return JsonResponse({"detail": "Invalid datetime format"}, status=400)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)

    hour = dt.hour
    is_bad_weather = 1 if weather in ["rain", "snow", "fog", "ice"] else 0

    prob = predict_probability(hour, traffic_density, is_bad_weather)

    cause = _classify_cause(hour, traffic_density, is_bad_weather)
    jam_level, jam_description = _classify_jam(prob, traffic_density)

    log = PredictionLog.objects.create(
        latitude=latitude,
        longitude=longitude,
        road_segment=road_segment,
        datetime=dt,
        weather=weather,
        traffic_density=traffic_density,
        accident_probability=prob,
        predicted_cause=cause,
        jam_level=jam_level,
    )

    return JsonResponse(
        {
            "probability": prob,
            "probability_percent": round(prob * 100, 1),
            "cause": cause,
            "jam_level": jam_level,
            "jam_description": jam_description,
            "log_id": log.id,
        }
    )
