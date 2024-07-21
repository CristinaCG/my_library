from django.test import TestCase
from ..models import Author, Book, Genre, Language, BookSaga, UserBookRelation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your tests here.

class GenreModelTest(TestCase):
    """
    Test the Genre model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        Genre.objects.create(name='Science Fiction')

    def setUp(self):
        self.genre = Genre.objects.create(name='Romance')

    def test_genre_name_label(self):
        """
        Test the genre name label
        """
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_genre_name(self):
        """ 
        Test the genre name
        """
        genre = Genre.objects.get(id=1)
        self.assertEqual(genre.name, 'Science Fiction')

    def test_genre_str_method(self):
        """
        Test the genre str method
        """
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), 'Science Fiction')

    def test_genre_update(self):
        """
        Change the genre name
        """
        self.genre.name = 'History'
        self.genre.save()
        self.assertEqual(self.genre.name, 'History')

    def test_genre_delete(self):
        """
        Delete the genre
        """
        num_of_genres = Genre.objects.all().count()
        self.genre.delete()
        self.assertEqual(Genre.objects.all().count(), num_of_genres-1)

    def test_genre_name_max_length(self):
        """
        Test the maximum length of the genre name
        """
        max_length = self.genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
        with self.assertRaises(ValidationError) as e:
            Genre.objects.create(name='a' * (max_length + 1))
        self.assertIn("Genre is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

    def test_genre_name_empty(self):
        """
        Test the minimum length of the genre name
        """
        with self.assertRaises(ValidationError) as e:
            Genre.objects.create(name='')
        self.assertIn("Genre cannot be empty", e.exception.message_dict["__all__"][0])

class LanguageModelTest(TestCase):
    """
    Test the Language model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        Language.objects.create(name='English')

    def setUp(self):
        self.language = Language.objects.create(name='France')

    def test_language_name_label(self):
        """
        Test the language name label
        """
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_language_name(self):
        """
        Test the language name
        """
        language = Language.objects.get(id=1)
        self.assertEqual(language.name, 'English')

    def test_language_str_method(self):
        """
        Test the language str method
        """
        language = Language.objects.get(id=1)
        self.assertEqual(str(language), 'English')

    def test_language_update(self):
        """
        Change the language name
        """
        self.language.name = 'Spanish'
        self.language.save()
        self.assertEqual(self.language.name, 'Spanish')

    def test_language_delete(self):
        """
        Delete the language
        """
        num_of_languages = Language.objects.all().count()
        self.language.delete()
        self.assertEqual(Language.objects.all().count(), num_of_languages-1)

    def test_language_name_max_length(self):
        """
        Test the maximum length of the language name
        """
        max_length = self.language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
        with self.assertRaises(ValidationError) as e:
            Language.objects.create(name = 'a' * (max_length + 1))
        self.assertIn("Language is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

    def test_language_name_empty(self):
        """
        Test the minimum length of the language name
        """
        with self.assertRaises(Exception) as exception:
            Language.objects.create(name='')
        self.assertIn("Language cannot be empty.",
                      str(exception.exception))

class AuthorModelTest(TestCase):
    """
    Test the Author model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        Author.objects.create(first_name='Big', last_name='Bob')
        Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        Author.objects.create(first_name='Large', last_name='Mary', year_of_death=2022)
        Author.objects.create(first_name='Medium', last_name='Joe', year_of_birth=2000, year_of_death=2020)

    def setUp(self):
        """
        Set up the data
        """
        self.author = Author.objects.create(first_name='Katherine', last_name='Johnson',
                                            year_of_birth=1918, year_of_death=2020)

    # ------------------ Label tests ------------------
    def test_author_first_name_label(self):
        """
        Test the first name label
        """
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_author_last_name_label(self):
        """
        Test the last name label
        """
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_author_year_of_birth_label(self):
        """
        Test the year of birth label
        """
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('year_of_birth').verbose_name
        self.assertEqual(field_label, 'year of birth')

    def test_author_year_of_death_label(self):
        """
        Test the year of death label
        """
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('year_of_death').verbose_name
        self.assertEqual(field_label, 'year of death')

    def test_author_create(self):
        """
        Test create author with different configurations
        """
        author = Author.objects.get(id=1)
        self.assertEqual(author.first_name, 'Big')
        self.assertEqual(author.last_name, 'Bob')
        self.assertEqual(author.year_of_birth, None)
        self.assertEqual(author.year_of_death, None)
        author = Author.objects.get(id=2)
        self.assertEqual(author.first_name, 'Small')
        self.assertEqual(author.last_name, 'Sue')
        self.assertEqual(author.year_of_birth, 2000)
        self.assertEqual(author.year_of_death, None)
        author = Author.objects.get(id=4)
        self.assertEqual(author.first_name, 'Medium')
        self.assertEqual(author.last_name, 'Joe')
        self.assertEqual(author.year_of_birth, 2000)
        self.assertEqual(author.year_of_death, 2020)
        author = Author.objects.get(id=3)
        self.assertEqual(author.first_name, 'Large')
        self.assertEqual(author.last_name, 'Mary')
        self.assertEqual(author.year_of_birth, None)
        self.assertEqual(author.year_of_death, 2022)

    def test_author_str_method(self):
        """
        Test the author str method
        """
        self.assertEqual(str(self.author), 'Katherine Johnson')

    def test_author_update(self):
        """
        Change the author name
        """
        self.author.first_name = 'Big 2'
        self.author.last_name = 'Bob 2'
        self.author.year_of_birth = 2000
        self.author.year_of_death = 2020
        self.author.save()
        self.assertEqual(self.author.first_name, 'Big 2')
        self.assertEqual(self.author.last_name, 'Bob 2')
        self.assertEqual(self.author.year_of_birth, 2000)
        self.assertEqual(self.author.year_of_death, 2020)

    def test_author_delete(self):
        """
        Delete the author
        """
        number_of_authors = Author.objects.all().count()
        self.author.delete()
        self.assertEqual(Author.objects.all().count(), number_of_authors-1)

    def test_author_first_name_max_length(self):
        """
        Test the maximum length of the author first name
        """
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='a' * (max_length + 1), last_name='Bob')
        self.assertIn("First name is too long, maximum length",
                      e.exception.message_dict["__all__"][0])

    def test_author_last_name_max_length(self):
        """
        Test the maximum length of the author last name
        """
        max_length = self.author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='Big', last_name='a' * (max_length + 1))
        self.assertIn("Last name is too long, maximum length",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_future(self):
        """
        Test the year of birth in the future
        """
        self.author.year_of_birth = 4000
        with self.assertRaises(ValidationError) as e:
            self.author.save()
        self.assertIn("Year of birth cannot be in the future",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_negative(self):
        """
        Test the year of birth in the future
        """
        self.author.year_of_birth = -4000
        with self.assertRaises(ValidationError) as e:
            self.author.save()
        self.assertIn("Year of birth cannot be negative",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_death_future(self):
        """
        Test the year of death in the future
        """
        self.author.year_of_death = 4000
        with self.assertRaises(ValidationError) as e:
            self.author.save()
        self.assertIn("Year of death cannot be in the future",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_death_negative(self):
        """
        Test the year of death in the future
        """
        self.author.year_of_death = -4000
        with self.assertRaises(ValidationError) as e:
            self.author.save()
        self.assertIn("Year of death cannot be negative",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_after_death(self):
        """
        Test the year of birth after the year of death
        """
        self.author.year_of_birth = 2000
        self.author.year_of_death = 1999
        with self.assertRaises(ValidationError) as e:
            self.author.save()
        self.assertIn("Year of birth cannot be after year of death",
                      e.exception.message_dict["__all__"][0])

    def test_author_first_name_empty(self):
        """
        Test the minimum length of the author first name
        """
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='', last_name='Bob')
        self.assertIn("First name cannot be empty",
                            e.exception.message_dict["__all__"][0])

    def test_author_last_name_empty(self):
        """
        Test the minimum length of the author last name
        """
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='Big', last_name='')
        self.assertIn("Last name cannot be empty",
                                e.exception.message_dict["__all__"][0])

    def test_author_get_absolute_url(self):
        """
        Test the get_absolute_url method
        """
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/book_catalog/author/1')

    def test_author_ordering(self):
        """
        Test the ordering of the authors
        """
        author = []
        indices = [0,3,4,2,1] # order
        for i in indices:
            author.append(Author.objects.get(id=i+1))
        self.assertEqual(list(Author.objects.all()), author)

class BookSagaModelTest(TestCase):
    """
    Test the BookSaga model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        Author.objects.create(first_name='Big', last_name='Bob')
        BookSaga.objects.create(name='Big Saga', author=Author.objects.get(id=1))

    def setUp(self):
        self.author = Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        self.saga = BookSaga.objects.create(name='Small Saga', author=self.author)


    def test_saga_name_label(self):
        """
        Test the saga name label
        """
        saga = BookSaga.objects.get(id=1)
        field_label = saga._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_saga_author_label(self):
        """
        Test the saga author label
        """
        saga = BookSaga.objects.get(id=1)
        field_label = saga._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_saga_create(self):
        """
        Test the saga name
        """
        saga = BookSaga.objects.get(id=1)
        self.assertEqual(saga.name, 'Big Saga')
        self.assertEqual(saga.author, Author.objects.get(id=1))

    def test_saga_str_method(self):
        """
        Test the saga str method
        """
        saga = BookSaga.objects.get(id=1)
        self.assertEqual(str(saga), 'Big Saga')

    def test_saga_update(self):
        """
        Change the saga name
        """
        self.saga.name = 'Big Saga 23'
        self.saga.author = Author.objects.get(id=1)
        self.saga.save()
        self.assertEqual(self.saga.name, 'Big Saga 23')
        self.assertEqual(self.saga.author, Author.objects.get(id=1))

    def test_saga_delete(self):
        """
        Delete the saga
        """
        num_of_sagas = BookSaga.objects.all().count()
        self.saga.delete()
        self.assertEqual(BookSaga.objects.all().count(), num_of_sagas-1)

    def test_saga_delete_if_author_deleted(self):
        """
        Delete the saga if the author is deleted
        """
        self.author.delete()
        saga = BookSaga.objects.all().filter(name='Small Saga')
        self.assertEqual(saga.count(), 0)

    def test_saga_name_max_length(self):
        """
        Test the maximum length of the saga name
        """
        max_length = self.saga._meta.get_field('name').max_length
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name='a' * (max_length + 1),
                                    author=Author.objects.get(id=1))
        self.assertIn("Saga name is too long, maximum",
                      e.exception.message_dict["__all__"][0])

    def test_saga_name_empty(self):
        """
        Test the minimum length of the saga name
        """
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name='',
                                    author=Author.objects.get(id=1))
        self.assertIn("Saga cannot be empty", e.exception.message_dict["__all__"][0])

    def test_saga_author_null(self):
        """
        Test the author null
        """
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name='Big Saga 4', author=None)

    def test_saga_get_absolute_url(self):
        """
        Test the get_absolute_url method
        """
        self.assertEqual(self.saga.get_absolute_url(), '/book_catalog/saga/2')

    def test_saga_repeated(self):
        """
        Test the repeated saga
        """
        saga = BookSaga.objects.get(id=1)
        author = Author.objects.get(id=1)
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name=saga.name, author=author)
        self.assertIn("Book saga with this Name and Author already exists.",
                      e.exception.message_dict["__all__"][0])

class BookModelTest(TestCase):
    """
    Test the Book model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        author = Author.objects.create(first_name='Big', last_name='Bob')
        Book.objects.create(title='Big Book', author=author,)
        saga = BookSaga.objects.create(name='Big Saga', author=author)
        Book.objects.create(title='Small Book', author=author,
                            saga = saga, saga_volume=2)
        Book.objects.create(title='Medium Book', author=author,
                            saga = saga, saga_volume=3,
                            publish_date='2021-07-19',
                            isbn='1234567890123',)
        language = Language.objects.create(name='English')
        genre = Genre.objects.create(name='Science Fiction')
        Book.objects.create(title='Large Book', author=author,
                            saga = saga, saga_volume=4,
                            publish_date='2021-07-19',
                            isbn='1234567890123',
                            summary='Big Summary',
                            language=language)
        book = Book.objects.get(id=4)
        book.genre.add(genre)

    def setUp(self):
        self.author = Author.objects.create(first_name='Small', last_name='Bob')
        self.saga = BookSaga.objects.create(name='Small Saga', author=self.author)
        self.language = Language.objects.create(name='German')
        self.genre_0 = Genre.objects.create(name='Romance')
        self.genre_1 = Genre.objects.create(name='History')
        self.book = Book.objects.create(title='Large Book', author=self.author,
                            saga = self.saga, saga_volume=1,
                            publish_date='2021-07-19',
                            isbn='1234567890123',
                            summary='Big Summary',
                            language=self.language)
        self.book.genre.add(self.genre_0, self.genre_1)
        self.book.save()

    def test_book_title_label(self):
        """
        Test the book title label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_book_author_label(self):
        """
        Test the book author label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_book_summary_label(self):
        """
        Test the book summary label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_book_isbn_label(self):
        """
        Test the book isbn label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'isbn')

    def test_book_language_label(self):
        """
        Test the book language label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_book_genre_label(self):
        """
        Test the book genre label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_book_saga_label(self):
        """
        Test the book saga label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('saga').verbose_name
        self.assertEqual(field_label, 'saga')

    def test_book_saga_volume_label(self):
        """
        Test the book saga volume label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('saga_volume').verbose_name
        self.assertEqual(field_label, 'saga volume')

    def test_book_publish_date_label(self):
        """
        Test the book publish date label
        """
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('publish_date').verbose_name
        self.assertEqual(field_label, 'publish date')

    def test_book_create(self):
        """
        Test the book name
        """
        book_0 = Book.objects.get(id=1)
        self.assertEqual(book_0.title, 'Big Book')
        self.assertEqual(book_0.author, Author.objects.get(id=1))
        self.assertEqual(book_0.summary, None)
        self.assertEqual(book_0.isbn, None)
        self.assertEqual(book_0.language, None)
        self.assertEqual(book_0.genre.all().count(), 0)
        self.assertEqual(book_0.saga, None)
        self.assertEqual(book_0.saga_volume, None)
        book_1 = Book.objects.get(id=2)
        self.assertEqual(book_1.title, 'Small Book')
        self.assertEqual(book_1.author, Author.objects.get(id=1))
        self.assertEqual(book_1.summary, None)
        self.assertEqual(book_1.isbn, None)
        self.assertEqual(book_1.language, None)
        self.assertEqual(book_1.genre.all().count(), 0)
        self.assertEqual(book_1.saga, BookSaga.objects.get(id=1))
        self.assertEqual(book_1.saga_volume, 2)
        book_2 = Book.objects.get(id=3)
        self.assertEqual(book_2.title, 'Medium Book')
        self.assertEqual(book_2.author, Author.objects.get(id=1))
        self.assertEqual(book_2.summary, None)
        self.assertEqual(book_2.isbn, '1234567890123')
        self.assertEqual(book_2.language, None)
        self.assertEqual(book_2.genre.all().count(), 0)
        self.assertEqual(book_2.saga, BookSaga.objects.get(id=1))
        self.assertEqual(book_2.saga_volume, 3)
        book_3 = Book.objects.get(id=4)
        self.assertEqual(book_3.title, 'Large Book')
        self.assertEqual(book_3.author, Author.objects.get(id=1))
        self.assertEqual(book_3.summary, 'Big Summary')
        self.assertEqual(book_3.isbn, '1234567890123')
        self.assertEqual(book_3.language, Language.objects.get(id=1))
        self.assertEqual(book_3.genre.all()[0], Genre.objects.get(id=1))
        self.assertEqual(book_3.saga, BookSaga.objects.get(id=1))
        self.assertEqual(book_3.saga_volume, 4)

    def test_book_str_method(self):
        """
        Test the book str method
        """
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), 'Big Book')

    def test_book_update(self):
        """
        Change the book name
        """
        self.book.title = 'Big Book 2'
        self.book.author = Author.objects.get(id=1)
        self.book.saga = None
        self.book.saga_volume = None
        self.book.summary = 'Big Summary 2'
        self.book.publish_date = '2021-07-20'
        self.book.isbn = '1234567890124'
        self.book.language = Language.objects.get(id=1)
        self.book.genre.set([Genre.objects.get(id=1)])
        self.book.save()
        self.assertEqual(self.book.title, 'Big Book 2')
        self.assertEqual(self.book.author, Author.objects.get(id=1))
        self.assertEqual(self.book.summary, 'Big Summary 2')
        self.assertEqual(self.book.isbn, '1234567890124')
        self.assertEqual(self.book.language, Language.objects.get(id=1))
        self.assertEqual(self.book.genre.all()[0], Genre.objects.get(id=1))
        self.assertEqual(self.book.saga, None)
        self.assertEqual(self.book.saga_volume, None)

    def test_book_delete(self):
        """
        Delete the book
        """
        num_of_books = Book.objects.all().count()
        self.book.delete()
        self.assertEqual(Book.objects.all().count(), num_of_books-1)

    def test_book_title_max_length(self):
        """
        Test the maximum length of the book title
        """
        max_length = self.book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
        self.book.title = 'a' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Title is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

    def test_book_title_empty(self):
        """
        Test the minimum length of the book title
        """
        self.book.title = ''
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Title cannot be empty", e.exception.message_dict['__all__'][0])

    def test_book_saga_volume_empty(self):
        """
        Test the minimum length of the book saga volume
        """
        self.book.saga_volume = None
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Saga volume cannot be empty if saga is set",
                      e.exception.message_dict['__all__'][0])

    def test_book_saga_volume_unique_in_saga(self):
        """
        Test the unique volume in saga
        """
        with self.assertRaises(ValidationError) as e:
            Book.objects.create(title='Small Book 2', author=self.author,
                                saga=self.saga, saga_volume = 1)
        self.assertIn("Book with this Saga and Saga volume already exists",
                      e.exception.message_dict['__all__'][0])

    def test_book_saga_volume_without_saga(self):
        """
        Test the volume without saga
        """
        self.book.saga = None
        self.book.saga_volume = 1
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Saga cannot be empty if saga volume is set",
                      e.exception.message_dict['__all__'][0])

    def test_book_get_absolute_url(self):
        """
        Test the get_absolute_url method
        """
        self.assertEqual(self.book.get_absolute_url(), '/book_catalog/book/5')

    def test_book_display_author(self):
        """
        Test the display_author method
        """
        self.assertEqual(self.book.display_author(), 'S. Bob')

    def test_book_display_title(self):
        """
        Test the display_title method
        """
        self.assertEqual(self.book.display_title(), 'Large Book (Small Saga, #1)')
        self.book.saga = None
        self.book.saga_volume = None
        self.book.save()
        self.assertEqual(self.book.display_title(), 'Large Book')

    def test_book_author_saga(self):
        """
        Test the author saga be different to the book author
        """
        self.book.saga = BookSaga.objects.get(id=1)
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Saga author must be the same as the book author",
                      e.exception.message_dict['__all__'][0])

    def test_book_publish_date_future(self):
        """
        Test the publish date in the future
        """
        self.book.publish_date = '4000-07-19'
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Publish date cannot be in the future",
                      e.exception.message_dict['__all__'][0])

    def test_book_isbn_max_length(self):
        """
        Test the maximum length of the book isbn
        """
        max_length = self.book._meta.get_field('isbn').max_length
        self.book.isbn = '1' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("ISBN must have 13 characters",
                      e.exception.message_dict['__all__'][0])

    def test_book_summary_max_length(self):
        """
        Test the maximum length of the book summary
        """
        max_length = self.book._meta.get_field('summary').max_length
        self.book.summary = 'a' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book.save()
        self.assertIn("Summary is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

    def test_book_duplicate(self):
        """
        Test the duplicate book
        """
        with self.assertRaises(ValidationError) as e:
            Book.objects.create(title='Large Book', author=self.author)
        self.assertIn("Book with this Title and Author already exists",
                      e.exception.message_dict['__all__'][0])

class UserBookRelationModelTest(TestCase):
    """
    Test the UserBookRelation model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up the permanent data
        """
        author = Author.objects.create(first_name='Big', last_name='Bob')
        book = Book.objects.create(title='Big Book', author=author)
        user = User.objects.create_user(username='testuser', password='12345')
        UserBookRelation.objects.create(user=user,
                                        book=book, status='r')

    def setUp(self):
        """
        Set up the data
        """
        self.author = Author.objects.create(first_name='Small', last_name='Bob')
        self.book = Book.objects.create(title='Small Book', author=self.author)
        self.user = User.objects.create_user(username='testuser_small', password='12345')
        self.user_book_relation = UserBookRelation.objects.create(user=self.user,
                                                                book=self.book, status='t')

    def test_user_book_relation_user_label(self):
        """
        Test the user label
        """
        user = User.objects.get(username='testuser')
        book = Book.objects.get(id=1)
        user_book_relation = UserBookRelation.objects.filter(user=user, book=book).first()
        field_label = user_book_relation._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_user_book_relation_book_label(self):
        """
        Test the book label
        """
        user = User.objects.get(username='testuser')
        book = Book.objects.get(id=1)
        user_book_relation = UserBookRelation.objects.filter(user=user, book=book).first()
        field_label = user_book_relation._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_user_book_relation_status_label(self):
        """
        Test the status label
        """
        user = User.objects.get(username='testuser')
        book = Book.objects.get(id=1)
        user_book_relation = UserBookRelation.objects.filter(user=user, book=book).first()
        field_label = user_book_relation._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_user_book_relation_create(self):
        """
        Test the user book relation
        """
        user = User.objects.get(username='testuser')
        book = Book.objects.get(id=1)
        user_book_relation = UserBookRelation.objects.filter(user=user, book=book).first()
        self.assertEqual(user_book_relation.user, user)
        self.assertEqual(user_book_relation.book, book)
        self.assertEqual(user_book_relation.status, 'r')

    def test_user_book_relation_str_method(self):
        """
        Test the user book relation str method
        """
        user = User.objects.get(username='testuser')
        book = Book.objects.get(id=1)
        user_book_relation = UserBookRelation.objects.filter(user=user, book=book).first()
        self.assertEqual(str(user_book_relation), 'testuser (Big Book)')

    def test_user_book_relation_update(self):
        """
        Change the user book relation
        """
        self.user_book_relation.status = 'i'
        self.user_book_relation.save()
        self.assertEqual(self.user_book_relation.status, 'i')

    def test_user_book_relation_delete(self):
        """
        Delete the user book relation
        """
        num_of_relations = UserBookRelation.objects.all().count()
        self.user_book_relation.delete()
        self.assertEqual(UserBookRelation.objects.all().count(), num_of_relations-1)

    def test_user_book_relation_invalid_status(self):
        """
        Test the maximum length of the user book relation status
        """
        self.user_book_relation.status = 'a'
        with self.assertRaises(ValidationError) as e:
            self.user_book_relation.save()
        self.assertIn("Invalid status",
                      e.exception.message_dict['__all__'][0])

    def test_user_book_relation_unique(self):
        """
        Test the unique user book relation
        """
        with self.assertRaises(ValidationError) as e:
            UserBookRelation.objects.create(user=self.user, book=self.book, status='r')
        self.assertIn("User book relation with this User and Book already exists",
                      e.exception.message_dict['__all__'][0])
