import os, argparse
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_library.settings'

import django
django.setup()

import book_catalog.models as models

def add_data():
    print("Creating data...")
    genre_romance = models.Genre.objects.create(name="Romance")
    genre_fiction = models.Genre.objects.create(name="Fiction")
    genre_contemporary = models.Genre.objects.create(name="Contemporary")
    genre_adult = models.Genre.objects.create(name="Adult")
    language_french = models.Language.objects.create(name="French")
    language_english = models.Language.objects.create(name="English")
    language_german = models.Language.objects.create(name="German")
    language_italian = models.Language.objects.create(name="Italian")
    language_spanish = models.Language.objects.create(name="Spanish")
    # Añade tus datos aquí. Por ejemplo:
    author = []
    author.append(models.Author.objects.create(first_name='Katherine', last_name='Center'))     # 0
    author.append(models.Author.objects.create(first_name='Elisabet', last_name='Benavent'))    # 1
    author.append(models.Author.objects.create(first_name='Amy', last_name='Tintera'))          # 2
    author.append(models.Author.objects.create(first_name='Jacobs', last_name='Anne'))          # 3
    author.append(models.Author.objects.create(first_name='Moreno', last_name='Eloy'))          # 4
    author.append(models.Author.objects.create(first_name='Gallego', last_name='Laura'))        # 5
    book = []
    book.append(models.Book.objects.create(title='La Guarda Espaldas', author=author[0], publish_date='2022-07-19', 
                                           summary = "PROTEGE A TU CLIENTE. PERO, POR ENCIMA DE TODO, PROTEGE TU CORAZÓN. La reina de las novelas reconfortantes llega a España con una historia sobre una guardaespaldas que no esperaba tener que fingir ser la novia de su próximo cliente... ni enamorarse de él. Ella tiene una misión. Hannah Brooks parece más una profesora de infantil que alguien que podría matarte con una servilleta, pero en realidad es guardaespaldas y acaban de asignarle una nueva misió proteger al actor superestrella Jack Stapleton de la señora que lo acosa y que se dedica a tejerle jerséis y a criar corgis. Él tiene su corazón. Jack Stapleton estaba en boca de todos y sus fotos, normalmente en playas paradisiacas, surcando las olas como un dios griego, saturaban las revistas de todo el país. Sin embargo, tras una tragedia familiar hace dos años, se alejó de los focos. Ambos tienen un secreto. Cuando la madre de Jack enferma, él vuelve al rancho familiar en Houston, Texas. Solo hay un pequeño Jack no quiere que su familia se entere de que necesita guardaespaldas. Así que, a regañadientes, Hannah accede a fingir que es su novia como tapadera. ¿Qué podría salir mal? Sin embargo, a medida que Hannah y Jack pasan tiempo juntos, ella empieza a pensar que todo parece casi… real. Y es entonces cuando las cosas comienzan a complicarse, porque para Hannah es pan comido mantener a salvo a Jack, pero es otra historia proteger su propio corazón de él.",
                                           language = language_german))
    book.append(models.Book.objects.create(title='Todas estas cosas que te diré mañana', author=author[1], publish_date='2022-07-19', language = language_spanish))
    
    saga_ruina = models.BookSaga.objects.create(name='Ruina', author=author[2])
    book.append(models.Book.objects.create(title='Alianza', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 1))
    book.append(models.Book.objects.create(title='Venganza', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 2))
    book.append(models.Book.objects.create(title='Ruina', author=author[2], publish_date='2022-07-19', saga = saga_ruina, saga_volume = 3))
    
    saga_la_villa_de_las_telas = models.BookSaga.objects.create(name='La villa de las telas', author=author[3])
    book.append(models.Book.objects.create(title='La villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 1))
    book.append(models.Book.objects.create(title='Las hijas de la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 2))
    book.append(models.Book.objects.create(title='El legado de la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 3))
    book.append(models.Book.objects.create(title='Regreso a la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 4))
    book.append(models.Book.objects.create(title='Tormenta en la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 5))
    book.append(models.Book.objects.create(title='Reencuentro en la villa de las telas', author=author[3], publish_date='2022-07-19', saga = saga_la_villa_de_las_telas, saga_volume = 6))
    
    book.append(models.Book.objects.create(title='El regalo', author=author[4], publish_date='2022-07-19', language = language_spanish))
    
    saga_memorias_de_idhun = models.BookSaga.objects.create(name="Memorias de Idhún", author=author[5])
    book.append(models.Book.objects.create(title='La resistencia', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 1))
    book.append(models.Book.objects.create(title='Tríada', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 2))
    book.append(models.Book.objects.create(title='Panteón', author=author[5], publish_date='2022-07-19', language = language_spanish, saga = saga_memorias_de_idhun, saga_volume = 3))

def clear_data():
    print("Deleting data...")
    # Borra tus datos aquí. Por ejemplo:
    models.Book.objects.all().delete()
    models.Author.objects.all().delete()
    models.Language.objects.all().delete()
    models.Genre.objects.all().delete()
    models.BookSaga.objects.all().delete()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['add_data', 'clear_data'])
    args = parser.parse_args()

    if args.command == 'add_data':
        add_data()
    elif args.command == 'clear_data':
        clear_data()