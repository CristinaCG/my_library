from django.test import TestCase
from .models import Author, Book, Genre, Language, BookSaga
# Create your tests here.

class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Language.objects.create(name='English')

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    
    def test_language_name_case_insensitive_unique(self):
        with self.assertRaises(Exception):
            Language.objects.create(name='english')
"""
    def test_get_absolute_url(self):
        language = Language.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(language.get_absolute_url(), '/book_catalog/language/1')
"""

class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Genre.objects.create(name='Science Fiction')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')
        Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        Author.objects.create(first_name='Medium', last_name='Joe', year_of_birth=2000, year_of_death=2020)

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_year_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('year_of_death').verbose_name
        self.assertEqual(field_label, 'year of death')

    def test_year_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('year_of_birth').verbose_name
        self.assertEqual(field_label, 'year of birth')
    
    def test_year_of_birth_null(self):
        author = Author.objects.get(id=1)
        field_null = author._meta.get_field('year_of_birth').null
        self.assertEqual(field_null, True)
    
    def test_year_of_death_null(self):
        author = Author.objects.get(id=1)
        field_null = author._meta.get_field('year_of_death').null
        self.assertEqual(field_null, True)
    
    def test_year_of_birth_future(self):
        with self.assertRaises(Exception):
            Author.objects.create(first_name='Big', last_name='Bob', year_of_birth=4000)

    def test_year_of_birth_negative(self):
        with self.assertRaises(Exception):
            Author.objects.create(first_name='Big', last_name='Bob', year_of_birth=-1)

    def test_year_of_death_future(self):
        with self.assertRaises(Exception):
            Author.objects.create(first_name='Big', last_name='Bob', year_of_death=4000)

    def test_year_of_death_negative(self):
        with self.assertRaises(Exception):
            Author.objects.create(first_name='Big', last_name='Bob', year_of_death=-1)

    def test_year_of_birth_after_death(self):
        with self.assertRaises(Exception):
            Author.objects.create(first_name='Big', last_name='Bob', year_of_birth=2000, year_of_death=1999)
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/book_catalog/author/1')

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        author = Author.objects.create(first_name='Big', last_name='Bob')
        genre = Genre.objects.create(name='Science Fiction')
        language = Language.objects.create(name='English')
        book = Book.objects.create(title='Big Book', author=author, summary='Big Summary', isbn='1234567890123', language=language)
        book.genre.set([genre])
        saga = BookSaga.objects.create(name='Big Saga', author=Author.objects.get(id=1))

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'isbn')

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_saga_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('saga').verbose_name
        self.assertEqual(field_label, 'saga')
    
    def test_saga_volume(self):
        with self.assertRaises(Exception):
            book = Book.objects.create(title='Big Book', author=Author.objects.get(id=1), summary='Big Summary', isbn='1234567890123', language=Language.objects.get(id=1),
                            saga=BookSaga.objects.get(id=1))

    def test_volume_unique_in_saga(self):
        Book.objects.create(title='Book 1', author=Author.objects.get(id=1), saga=BookSaga.objects.get(id=1), saga_volume=1, language = Language.objects.get(id=1))
        with self.assertRaises(Exception):
            Book.objects.create(title='Book 2', author=Author.objects.get(id=1), saga=BookSaga.objects.get(id=1), saga_volume=1, language = Language.objects.get(id=1))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(book.get_absolute_url(), '/book_catalog/book/1')

class BookSagaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        author = Author.objects.create(first_name='Big', last_name='Bob')
        saga = BookSaga.objects.create(name='Big Saga', author=author)
        language = Language.objects.create(name='English')
        Book.objects.create(title='Big Book', author=author, summary='Big Summary', isbn='1234567890123', saga = saga, saga_volume = 1, language = language)
        
    def test_name_label(self):
        saga = BookSaga.objects.get(id=1)
        field_label = saga._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        saga = BookSaga.objects.get(id=1)
        max_length = saga._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_author_label(self):
        saga = BookSaga.objects.get(id=1)
        field_label = saga._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_author_null(self):
        saga = BookSaga.objects.get(id=1)
        field_null = saga._meta.get_field('author').null
        self.assertEqual(field_null, False)
    
    def test_get_absolute_url(self):
        saga = BookSaga.objects.get(id=1)
        self.assertEqual(saga.get_absolute_url(), '/book_catalog/saga/1')