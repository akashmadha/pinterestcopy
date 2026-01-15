from django.apps import AppConfig


class PinterestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pinterest_App'
    
    def ready(self):
        # Import signals to register them
        import pinterest_App.signals

