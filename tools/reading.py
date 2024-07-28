import os
import sys
import django

# Configura el entorno Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_library.settings'
django.setup()

from django.contrib.auth.models import User
from book_catalog.models import Book, UserBookRelation
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

# Función para generar una fecha aleatoria dentro de un rango dado
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Recuperar usuarios y libros
users = User.objects.all()
books = Book.objects.all()

# Verifica que haya datos en la base de datos
if not users.exists() or not books.exists():
    print("No hay usuarios o libros en la base de datos.")
else:
    created_count = 0
    attempts = 0
    max_entries = 5000 # Número de entradas a crear
    max_attempts = 10000  # Número máximo de intentos para encontrar combinaciones únicas

    while created_count < max_entries and attempts < max_attempts:
        user = random.choice(users)
        book = random.choice(books)

        # Verifica si ya existe una entrada para esta combinación
        if not UserBookRelation.objects.filter(user=user, book=book).exists():
            status = random.choice(['r', 't', 'i'])
            reading_date = random_date(datetime(2022, 1, 1), datetime(2024, 7, 1)) if status == 'i' else None
            read_date = random_date(datetime(2022, 1, 1), datetime(2024, 7, 1)) if status == 'r' else None
            rating = random.randint(1, 5) if status == 'r' else None
            review = f"This is a review for the book {book.title} by user {user.username}." if status == 'r' else None
            review_date = read_date if status == 'r' else None

            UserBookRelation.objects.create(
                user=user,
                book=book,
                status=status,
                reading_date=make_aware(reading_date) if reading_date else None,
                read_date=make_aware(read_date) if read_date else None,
                rating=rating,
                review=review,
                review_date=make_aware(review_date) if review_date else None
            )

            created_count += 1
        attempts += 1

    if created_count == max_entries:
        print(f"{created_count} entradas creadas exitosamente.")
    else:
        print(f"No se pudieron crear 100 entradas únicas. Se crearon {created_count} entradas.")
