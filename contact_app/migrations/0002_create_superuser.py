from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='niyadfreelancer@gmail.com',
            password='Reymysterio9501#'  # Replace with a strong password
        )

class Migration(migrations.Migration):
    dependencies = [
        ('contact_app', '0001_initial'),  # Adjust to match your last migration
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]