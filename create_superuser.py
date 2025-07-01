import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contact_backend.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="niyad").exists():
    User.objects.create_superuser(
        username="niyad",
        email="sunilniyad@gmail.com",
        password=os.environ.get("DJNAGO_SUPERUSER_PASSWORD", "your_secure_password")
    )
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")