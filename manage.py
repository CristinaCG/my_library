#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management.base import BaseCommand
import book_catalog.models as models


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_library.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# class Command(BaseCommand):
#     help = 'Creates random users'

#     def handle(self, *args, **kwargs):
#         # Crea tus datos aquí. Por ejemplo:
#         author = models.Author.objects.create(name='Test Author', year_of_birth=1980)
#         book = models.Book.objects.create(title='Test Book', author=author, publish_date='2021-01-01')
#         self.stdout.write(self.style.SUCCESS('Data created successfully'))


if __name__ == '__main__':
    main()
