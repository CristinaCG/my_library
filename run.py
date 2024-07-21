import os
import argparse
import django
# from django.contrib.auth.models import User
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_library.settings'
django.setup()
from django.contrib.auth.models import Permission, Group, User
import book_catalog.models as book_catalog_models


def clear_data():
    print("Deleting data...")
    # Borra tus datos aquí. Por ejemplo:
    book_catalog_models.Book.objects.all().delete()
    book_catalog_models.Author.objects.all().delete()
    book_catalog_models.Language.objects.all().delete()
    book_catalog_models.Genre.objects.all().delete()
    book_catalog_models.BookSaga.objects.all().delete()
    book_catalog_models.User.objects.all().delete()
    book_catalog_models.UserBookRelation.objects.all().delete()

def add_data():
    clear_data()
    print("Creating data...")
    genre_romance = book_catalog_models.Genre.objects.create(name="Romance")
    genre_fiction = book_catalog_models.Genre.objects.create(name="Fiction")
    genre_contemporary = book_catalog_models.Genre.objects.create(name="Contemporary")
    genre_adult = book_catalog_models.Genre.objects.create(name="Adult")
    language_french = book_catalog_models.Language.objects.create(name="French")
    language_english = book_catalog_models.Language.objects.create(name="English")
    language_german = book_catalog_models.Language.objects.create(name="German")
    language_italian = book_catalog_models.Language.objects.create(name="Italian")
    language_spanish = book_catalog_models.Language.objects.create(name="Spanish")
    # Añade tus datos aquí. Por ejemplo:
    author = []
    author.append(book_catalog_models.Author.objects.create(first_name='Katherine', last_name='Center'), year_of_birth = 1972)     # 0
    author.append(book_catalog_models.Author.objects.create(first_name='Elisabet', last_name='Benavent'), year_of_birth=1984)    # 1
    author.append(book_catalog_models.Author.objects.create(first_name='Amy', last_name='Tintera'))          # 2
    author.append(book_catalog_models.Author.objects.create(first_name='Jacobs', last_name='Anne', year_of_birth=1941))         # 3
    author.append(book_catalog_models.Author.objects.create(first_name='Moreno', last_name='Eloy', year_of_birth=1976))          # 4
    author.append(book_catalog_models.Author.objects.create(first_name='Gallego', last_name='Laura', year_of_birth=1977))
    author.append(book_catalog_models.Author.objects.create(first_name='Asimov', last_name='Isaac', year_of_death=1992))
    book = []
    book.append(book_catalog_models.Book.objects.create(title='La Guarda Espaldas', author=author[0], publish_date='2022-07-19', 
                                           summary = "PROTEGE A TU CLIENTE. PERO, POR ENCIMA DE TODO, PROTEGE TU CORAZÓN. La reina de las novelas reconfortantes llega a España con una .",
                                           language = language_german))
    book.append(book_catalog_models.Book.objects.create(title='Todas estas cosas que te diré mañana', author=author[1], publish_date='2022-07-19', language = language_spanish))
    
    saga_ruina = book_catalog_models.BookSaga.objects.create(name='Ruina', author=author[2])
    book.append(book_catalog_models.Book.objects.create(title='Alianza', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 1))
    book.append(book_catalog_models.Book.objects.create(title='Venganza', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 2))
    book.append(book_catalog_models.Book.objects.create(title='Ruina', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 3))
    
    saga_la_villa_de_las_telas = book_catalog_models.BookSaga.objects.create(name='La villa de las telas', author=author[3])
    book.append(book_catalog_models.Book.objects.create(title='La villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 1))
    book.append(book_catalog_models.Book.objects.create(title='Las hijas de la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 2))
    book.append(book_catalog_models.Book.objects.create(title='El legado de la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 3))
    book.append(book_catalog_models.Book.objects.create(title='Regreso a la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 4))
    book.append(book_catalog_models.Book.objects.create(title='Tormenta en la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 5))
    book.append(book_catalog_models.Book.objects.create(title='Reencuentro en la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 6))
    
    book.append(book_catalog_models.Book.objects.create(title='El regalo', author=author[4], publish_date='2022-07-19', language = language_spanish))
    
    saga_memorias_de_idhun = book_catalog_models.BookSaga.objects.create(name="Memorias de Idhún", author=author[5])
    book.append(book_catalog_models.Book.objects.create(title='La resistencia', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 1))
    book.append(book_catalog_models.Book.objects.create(title='Tríada', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 2))
    book.append(book_catalog_models.Book.objects.create(title='Panteón', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 3))

    superuser = User.objects.create_superuser('admin', 'correo@ejemplo.com', '1234')
    superuser.save()

    user1 = User.objects.create_user(username = 'julio', email = 'myemail@crazymail.com', password = 'julio')
    user1.first_name = 'Julio'
    user1.last_name = 'García'
    user1.save()

    user2 = User.objects.create_user(username = 'teresa', email = 'myemail@crazymail.com', password = 'teresa')
    user2.first_name = 'Teresa'
    user2.last_name = 'Aranda'
    user2.save()

    # Create group of user
    Group.objects.create(name='staff')
    models_list = ['author', 'book', 'book saga', 'genre', 'language']
    # proj_add_perm = [0]*(len(models_list)*4)
    actions = ['add', 'change', 'delete', 'view']
    for action in actions:
        for model in models_list:
            perm = Permission.objects.get(name=f'Can {action} {model}')
            group = Group.objects.get(name='staff')
            group.permissions.add(perm)

    user_staff_1 = User.objects.create_user(username = 'staff1', email = 'staff1@crazymail.com', password='staff1')
    user_staff_2 = User.objects.create_user(username = 'staff2', email = 'staff2@crazymail.com', password='staff2')
    user_staff_1.first_name = 'Staff'
    user_staff_1.last_name = 'One'
    user_staff_2.first_name = 'Staff'
    user_staff_2.last_name = 'Two'
    user_staff_1.groups.add(Group.objects.get(name='staff'))
    user_staff_2.groups.add(Group.objects.get(name='staff'))
    user_staff_1.save()
    user_staff_2.save()

    state1 = book_catalog_models.UserBookRelation.objects.create(user = user1, book = book[0], status = 'r')
    state2 = book_catalog_models.UserBookRelation.objects.create(user = user1, book = book[1], status = 'r')
    state3 = book_catalog_models.UserBookRelation.objects.create(user = user2, book = book[2], status = 'i')
    state4 = book_catalog_models.UserBookRelation.objects.create(user = user2, book = book[3], status = 't')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['add_data', 'clear_data'])
    args = parser.parse_args()

    if args.command == 'add_data':
        add_data()
    elif args.command == 'clear_data':
        clear_data()