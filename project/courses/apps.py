from django.apps import AppConfig

# Тут автоматически прописываются настройки приложения
class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
