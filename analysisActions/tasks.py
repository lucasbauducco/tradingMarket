from celery import shared_task
import requests

@shared_task
def actualizar_cedears_task():
    url = 'http://127.0.0.1:8000//api/actualizar-cedears/'
    response = requests.get(url)
    return response.text