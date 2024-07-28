import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_library.settings'
django.setup()

from django.contrib.auth.models import Group, User
import book_catalog.models as book_catalog_models

print("Deleting data...")
book_catalog_models.Book.objects.all().delete()
book_catalog_models.Author.objects.all().delete()
book_catalog_models.Language.objects.all().delete()
book_catalog_models.Genre.objects.all().delete()
book_catalog_models.BookSaga.objects.all().delete()
book_catalog_models.User.objects.all().delete()
book_catalog_models.UserBookRelation.objects.all().delete()
Group.objects.all().delete()
User.objects.all().delete()