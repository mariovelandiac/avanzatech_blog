import os
from user.models import CustomUser

def check_and_create_superuser():
    # Get superuser credentials from environment variables
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

    # Check if superuser already exists
    if not CustomUser.objects.filter(is_superuser=True).exists():
        # Create superuser
        print("Creating superuser...")
        CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )


check_and_create_superuser()