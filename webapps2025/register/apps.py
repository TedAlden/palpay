from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.conf import settings


def create_default_superuser(**kwargs):
    """Creates a default superuser if one does not already exist.

    Uses the credentials defined in the settings file:
    - DEFAULT_SUPERUSER_USERNAME
    - DEFAULT_SUPERUSER_PASSWORD
    - DEFAULT_SUPERUSER_EMAIL
    """
    User = get_user_model()

    # Check if a superuser doesn't already exist
    if not User.objects.filter(username=settings.DEFAULT_SUPERUSER_USERNAME).exists():
        # Create a superuser account with default credentials
        User.objects.create_superuser(
            username=settings.DEFAULT_SUPERUSER_USERNAME,
            password=settings.DEFAULT_SUPERUSER_PASSWORD,
            email=settings.DEFAULT_SUPERUSER_EMAIL,
        )
        print("Successfully created default superuser account.")


class RegisterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "register"

    def ready(self):
        # Create the default superuser when migrating. When running:
        # $ python manage.py migrate register
        post_migrate.connect(create_default_superuser, sender=self)
