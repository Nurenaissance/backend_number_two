import sys
import os
import django

# Step 1: Add Django Project to Python Path
# Adjust the path to point to your Django project directory
sys.path.append("D:\\new_nurenai\\newwwwwwwwwwwwwwwwwwww\\backend_mine")  # Absolute path to your Django project folder


# Step 2: Set DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplecrm.settings')  # Replace with your Django settings module
# Step 3: Initialize Django
django.setup()
