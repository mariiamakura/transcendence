from django.apps import AppConfig
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pong.settings')


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'
