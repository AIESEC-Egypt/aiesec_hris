from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'aiesec_hris.users'
    verbose_name = "Users"

    def ready(self):
        pass
