from django.apps import AppConfig

class DjangoBridgeProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_bridge_project' # Make sure this matches your app's name in INSTALLED_APPS

    def ready(self):
        import django_bridge_project.signals # Import your signals module 