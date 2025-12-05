from django.urls import path
from .views import predict_accident

urlpatterns = [
    path("predict/", predict_accident, name="predict_accident"),
]
