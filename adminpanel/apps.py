from django.apps import AppConfig


class AdminpanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "adminpanel"
    verbose_name = 'Painel Administrativo'
    
    def ready(self):
        """Configurações quando a app estiver pronta"""
        # Não registrar models automaticamente
        # O registro será feito nas URLs ou manualmente
        pass
