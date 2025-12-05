from django.db import models

class PredictionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    road_segment = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField()
    weather = models.CharField(max_length=50)
    traffic_density = models.FloatField()
    accident_probability = models.FloatField()
    predicted_cause = models.CharField(max_length=255)
    jam_level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.datetime} - {self.road_segment or 'segment'}"
