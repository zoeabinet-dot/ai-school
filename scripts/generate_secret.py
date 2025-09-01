"""Utility: generate a Django-compatible SECRET_KEY

Run locally and copy the output into your environment or GitHub Secret.
Example:
  python scripts/generate_secret.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    print(get_random_secret_key())
