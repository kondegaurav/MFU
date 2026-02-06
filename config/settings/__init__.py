# Settings package for MFU Web Portal
# Import the appropriate settings module based on DJANGO_SETTINGS_MODULE env variable
# Default to development if not specified
import os

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
