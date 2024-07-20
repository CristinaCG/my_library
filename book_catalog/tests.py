from django.test import TestCase
from .models import Author, Book, Genre, Language, BookSaga, UserBookRelation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your tests here.

class GenreModelTest(TestCase):
    """
    Test the Genre model
    """
    def setUp(self):
        self.genre = Genre.objects.create(name='Science Fiction')

    def test_genre_name(self):
        """ 
        Test the genre name
        """
        self.assertEqual(self.genre.name, 'Science Fiction')

    def test_genre_str_method(self):
        """
        Test the genre str method
        """
        self.assertEqual(str(self.genre), 'Science Fiction')

    def test_genre_update(self):
        """
        Change the genre name
        """
        self.genre.name = 'Science Fiction 2'
        self.genre.save()
        self.assertEqual(self.genre.name, 'Science Fiction 2')

    def test_genre_delete(self):
        """
        Delete the genre
        """
        self.genre.delete()
        self.assertEqual(Genre.objects.all().count(), 0)

    def test_genre_name_max_length(self):
        """
        Test the maximum length of the genre name
        """
        max_length = self.genre._meta.get_field('name').max_length
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
    def setUp(self):
        self.language = Language.objects.create(name='English')

    def test_language_name(self):
        """
        Test the language name
        """
        self.assertEqual(self.language.name, 'English')

    def test_language_str_method(self):
        """
        Test the language str method
        """
        self.assertEqual(str(self.language), 'English')

    def test_language_update(self):
        """
        Change the language name
        """
        self.language.name = 'English 2'
        self.language.save()
        self.assertEqual(self.language.name, 'English 2')

    def test_language_delete(self):
        """
        Delete the language
        """
        self.language.delete()
        self.assertEqual(Language.objects.all().count(), 0)

    def test_language_name_max_length(self):
        """
        Test the maximum length of the language name
        """
        max_length = self.language._meta.get_field('name').max_length
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
    def setUp(self):
        self.author_0 = Author.objects.create(first_name='Big', last_name='Bob')
        self.author_1 = Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        self.author_2 = Author.objects.create(first_name='Medium', last_name='Joe', year_of_birth=2000, year_of_death=2020)

    def test_author_create(self):
        """
        Test the author name
        """
        self.assertEqual(self.author_0.first_name, 'Big')
        self.assertEqual(self.author_0.last_name, 'Bob')
        self.assertEqual(self.author_0.year_of_birth, None)
        self.assertEqual(self.author_0.year_of_death, None)
        self.assertEqual(self.author_1.first_name, 'Small')
        self.assertEqual(self.author_1.last_name, 'Sue')
        self.assertEqual(self.author_1.year_of_birth, 2000)
        self.assertEqual(self.author_1.year_of_death, None)
        self.assertEqual(self.author_2.first_name, 'Medium')
        self.assertEqual(self.author_2.last_name, 'Joe')
        self.assertEqual(self.author_2.year_of_birth, 2000)
        self.assertEqual(self.author_2.year_of_death, 2020)

    def test_author_str_method(self):
        """
        Test the author str method
        """
        self.assertEqual(str(self.author_0), 'Big Bob')
        self.assertEqual(str(self.author_1), 'Small Sue')
        self.assertEqual(str(self.author_2), 'Medium Joe')

    def test_author_update(self):
        """
        Change the author name
        """
        self.author_0.first_name = 'Big 2'
        self.author_0.last_name = 'Bob 2'
        self.author_0.save()
        self.assertEqual(self.author_0.first_name, 'Big 2')
        self.assertEqual(self.author_0.last_name, 'Bob 2')

    def test_author_delete(self):
        """
        Delete the author
        """
        self.author_0.delete()
        self.assertEqual(Author.objects.all().count(), 2)

    def test_author_first_name_max_length(self):
        """
        Test the maximum length of the author first name
        """
        max_length = self.author_0._meta.get_field('first_name').max_length
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='a' * (max_length + 1), last_name='Bob')
        self.assertIn("First name is too long, maximum length",
                      e.exception.message_dict["__all__"][0])

    def test_author_last_name_max_length(self):
        """
        Test the maximum length of the author last name
        """
        max_length = self.author_0._meta.get_field('last_name').max_length
        with self.assertRaises(ValidationError) as e:
            Author.objects.create(first_name='Big', last_name='a' * (max_length + 1))
        self.assertIn("Last name is too long, maximum length",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_future(self):
        """
        Test the year of birth in the future
        """
        self.author_0.year_of_birth = 4000
        with self.assertRaises(ValidationError) as e:
            self.author_0.save()
        self.assertIn("Year of birth cannot be in the future",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_negative(self):
        """
        Test the year of birth in the future
        """
        self.author_0.year_of_birth = -4000
        with self.assertRaises(ValidationError) as e:
            self.author_0.save()
        self.assertIn("Year of birth cannot be negative",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_death_future(self):
        """
        Test the year of death in the future
        """
        self.author_0.year_of_death = 4000
        with self.assertRaises(ValidationError) as e:
            self.author_0.save()
        self.assertIn("Year of death cannot be in the future",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_death_negative(self):
        """
        Test the year of death in the future
        """
        self.author_0.year_of_death = -4000
        with self.assertRaises(ValidationError) as e:
            self.author_0.save()
        self.assertIn("Year of death cannot be negative",
                      e.exception.message_dict["__all__"][0])

    def test_author_year_of_birth_after_death(self):
        """
        Test the year of birth after the year of death
        """
        self.author_0.year_of_birth = 2000
        self.author_0.year_of_death = 1999
        with self.assertRaises(ValidationError) as e:
            self.author_0.save()
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
        self.assertEqual(self.author_0.get_absolute_url(), '/book_catalog/author/1')
        self.assertEqual(self.author_1.get_absolute_url(), '/book_catalog/author/2')
        self.assertEqual(self.author_2.get_absolute_url(), '/book_catalog/author/3')

    def test_author_ordering(self):
        """
        Test the ordering of the authors
        """
        self.assertEqual(list(Author.objects.all()), [self.author_0, self.author_2, self.author_1])

class BookSagaModelTest(TestCase):
    """
    Test the BookSaga model
    """
    def setUp(self):
        self.author_0 = Author.objects.create(first_name='Big', last_name='Bob')
        self.author_1 = Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        self.author_2 = Author.objects.create(first_name='Medium', last_name='Joe', year_of_birth=2000, year_of_death=2020)
        self.saga_0 = BookSaga.objects.create(name='Big Saga', author=self.author_0)
        self.saga_1 = BookSaga.objects.create(name='Big Saga 1', author=self.author_1)
        self.saga_2 = BookSaga.objects.create(name='Big Saga 2', author=self.author_1)
        self.saga_3 = BookSaga.objects.create(name='Big Saga 3', author=self.author_2)

    def test_saga_create(self):
        """
        Test the saga name
        """
        self.assertEqual(self.saga_0.name, 'Big Saga')
        self.assertEqual(self.saga_0.author, self.author_0)
        self.assertEqual(self.saga_1.name, 'Big Saga 1')
        self.assertEqual(self.saga_1.author, self.author_1)
        self.assertEqual(self.saga_2.name, 'Big Saga 2')
        self.assertEqual(self.saga_2.author, self.author_1)
        self.assertEqual(self.saga_3.name, 'Big Saga 3')
        self.assertEqual(self.saga_3.author, self.author_2)

    def test_saga_str_method(self):
        """
        Test the saga str method
        """
        self.assertEqual(str(self.saga_0), 'Big Saga')
        self.assertEqual(str(self.saga_1), 'Big Saga 1')
        self.assertEqual(str(self.saga_2), 'Big Saga 2')
        self.assertEqual(str(self.saga_3), 'Big Saga 3')

    def test_saga_update(self):
        """
        Change the saga name
        """
        self.saga_0.name = 'Big Saga 23'
        self.saga_0.save()
        self.assertEqual(self.saga_0.name, 'Big Saga 23')
        self.saga_0.author = self.author_2
        self.saga_0.save()
        self.assertEqual(self.saga_0.author, self.author_2)

    def test_saga_delete(self):
        """
        Delete the saga
        """
        self.saga_0.delete()
        self.assertEqual(BookSaga.objects.all().count(), 3)

    def test_saga_name_max_length(self):
        """
        Test the maximum length of the saga name
        """
        max_length = self.saga_0._meta.get_field('name').max_length
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name='a' * (max_length + 1), author=self.author_0)
        self.assertIn("Saga name is too long, maximum",
                      e.exception.message_dict["__all__"][0])

    def test_saga_name_empty(self):
        """
        Test the minimum length of the saga name
        """
        with self.assertRaises(ValidationError) as e:
            BookSaga.objects.create(name='', author=self.author_0)
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
        self.assertEqual(self.saga_0.get_absolute_url(), '/book_catalog/saga/1')
        self.assertEqual(self.saga_1.get_absolute_url(), '/book_catalog/saga/2')
        self.assertEqual(self.saga_2.get_absolute_url(), '/book_catalog/saga/3')
        self.assertEqual(self.saga_3.get_absolute_url(), '/book_catalog/saga/4')

class BookModelTest(TestCase):
    """
    Test the Book model
    """
    def setUp(self):
        self.author_0 = Author.objects.create(first_name='Big', last_name='Bob')
        self.author_1 = Author.objects.create(first_name='Small', last_name='Sue', year_of_birth=2000)
        self.author_2 = Author.objects.create(first_name='Medium', last_name='Joe',
                                              year_of_birth=2000, year_of_death=2020)
        self.genre_0 = Genre.objects.create(name='Science Fiction')
        self.genre_1 = Genre.objects.create(name='Romance')
        self.language_0 = Language.objects.create(name='English')
        self.language_1 = Language.objects.create(name='German')
        self.saga_0 = BookSaga.objects.create(name='Big Saga', author=self.author_0)
        self.saga_1 = BookSaga.objects.create(name='Big Saga 1', author=self.author_1)
        self.saga_2 = BookSaga.objects.create(name='Big Saga 2', author=self.author_1)
        self.saga_3 = BookSaga.objects.create(name='Big Saga 3', author=self.author_2)
        self.book_0 = Book.objects.create(title='Big Book', author=self.author_0,
                                          summary='Big Summary', isbn='1234567890123',
                                          language=self.language_0,
                                          saga = self.saga_0, saga_volume = 1)
        self.book_0.genre.set([self.genre_0])
        self.book_0.save()
        self.book_1 = Book.objects.create(title='Small Book', author=self.author_1,
                                          summary='Small Summary', isbn='1234567890124',
                                          language=self.language_1)
        self.book_1.genre.set([self.genre_1])
        self.book_1.saga = self.saga_1
        self.book_1.saga_volume = 2
        self.book_1.save()

    def test_book_create(self):
        """
        Test the book name
        """
        self.assertEqual(self.book_0.title, 'Big Book')
        self.assertEqual(self.book_0.author, self.author_0)
        self.assertEqual(self.book_0.summary, 'Big Summary')
        self.assertEqual(self.book_0.isbn, '1234567890123')
        self.assertEqual(self.book_0.language, self.language_0)
        self.assertEqual(self.book_0.genre.all()[0], self.genre_0)
        self.assertEqual(self.book_0.saga, self.saga_0)
        self.assertEqual(self.book_0.saga_volume, 1)
        self.assertEqual(self.book_1.title, 'Small Book')
        self.assertEqual(self.book_1.author, self.author_1)
        self.assertEqual(self.book_1.summary, 'Small Summary')
        self.assertEqual(self.book_1.isbn, '1234567890124')
        self.assertEqual(self.book_1.language, self.language_1)
        self.assertEqual(self.book_1.genre.all()[0], self.genre_1)
        self.assertEqual(self.book_1.saga, self.saga_1)
        self.assertEqual(self.book_1.saga_volume, 2)

    def test_book_str_method(self):
        """
        Test the book str method
        """
        self.assertEqual(str(self.book_0), 'Big Book')
        self.assertEqual(str(self.book_1), 'Small Book')

    def test_book_update(self):
        """
        Change the book name
        """
        self.book_0.saga = None
        self.book_0.saga_volume = None
        self.book_0.title = 'Big Book 2'
        self.book_0.save()
        self.assertEqual(self.book_0.title, 'Big Book 2')
        self.book_0.author = self.author_1
        self.book_0.save()
        self.assertEqual(self.book_0.author, self.author_1)
        self.book_0.summary = 'Big Summary 2'
        self.book_0.save()
        self.assertEqual(self.book_0.summary, 'Big Summary 2')
        self.book_0.isbn = '1234567890124'
        self.book_0.save()
        self.assertEqual(self.book_0.isbn, '1234567890124')
        self.book_0.language = self.language_1
        self.book_0.save()
        self.assertEqual(self.book_0.language, self.language_1)
        self.book_0.genre.set([self.genre_1])
        self.book_0.save()
        self.assertEqual(self.book_0.genre.all()[0], self.genre_1)
        self.book_0.saga = self.saga_1
        self.book_0.saga_volume = 1
        self.book_0.author = self.book_0.saga.author
        self.book_0.save()
        self.assertEqual(self.book_0.saga, self.saga_1)
        self.book_0.saga_volume = 3
        self.book_0.save()
        self.assertEqual(self.book_0.saga_volume, 3)

    def test_book_delete(self):
        """
        Delete the book
        """
        self.book_0.delete()
        self.assertEqual(Book.objects.all().count(), 1)

    def test_book_title_max_length(self):
        """
        Test the maximum length of the book title
        """
        max_length = self.book_0._meta.get_field('title').max_length
        self.book_0.title = 'a' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Title is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

    def test_book_title_empty(self):
        """
        Test the minimum length of the book title
        """
        self.book_0.title = ''
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Title cannot be empty", e.exception.message_dict['__all__'][0])

    def test_book_saga_volume_empty(self):
        """
        Test the minimum length of the book saga volume
        """
        self.book_0.saga_volume = None
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Saga volume cannot be empty if saga is set",
                      e.exception.message_dict['__all__'][0])

    def test_book_saga_volume_unique_in_saga(self):
        """
        Test the unique volume in saga
        """
        self.book_0.saga_volume = 2
        self.book_0.saga = self.saga_1
        self.book_0.author = self.book_0.saga.author
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Book with this Saga and Saga volume already exists",
                      e.exception.message_dict['__all__'][0])

    def test_book_get_absolute_url(self):
        """
        Test the get_absolute_url method
        """
        self.assertEqual(self.book_0.get_absolute_url(), '/book_catalog/book/1')
        self.assertEqual(self.book_1.get_absolute_url(), '/book_catalog/book/2')

    def test_book_display_author(self):
        """
        Test the display_author method
        """
        self.assertEqual(self.book_0.display_author(), 'B. Bob')
        self.assertEqual(self.book_1.display_author(), 'S. Sue')

    def test_book_display_title(self):
        """
        Test the display_title method
        """
        self.assertEqual(self.book_0.display_title(), 'Big Book (Big Saga, #1)')
        self.assertEqual(self.book_1.display_title(), 'Small Book (Big Saga 1, #2)')

    def test_book_author_saga(self):
        """
        Test the author saga be different to the book author
        """
        self.book_0.saga = self.saga_1
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Saga author must be the same as the book author",
                      e.exception.message_dict['__all__'][0])

    def test_book_publish_date_future(self):
        """
        Test the publish date in the future
        """
        self.book_0.publish_date = '4000-07-19'
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Publish date cannot be in the future",
                      e.exception.message_dict['__all__'][0])

    def test_book_isbn_max_length(self):
        """
        Test the maximum length of the book isbn
        """
        max_length = self.book_0._meta.get_field('isbn').max_length
        self.book_0.isbn = '1' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("ISBN must have 13 characters",
                      e.exception.message_dict['__all__'][0])

    def test_book_summary_max_length(self):
        """
        Test the maximum length of the book summary
        """
        max_length = self.book_0._meta.get_field('summary').max_length
        self.book_0.summary = 'a' * (max_length + 1)
        with self.assertRaises(ValidationError) as e:
            self.book_0.save()
        self.assertIn("Summary is too long, maximum length",
                      e.exception.message_dict['__all__'][0])

class UserBookRelationModelTest(TestCase):
    """
    Test the UserBookRelation model
    """
    def setUp(self):
        """
        Set up the data
        """
        self.author_0 = Author.objects.create(first_name='Big', last_name='Bob')
        self.genre_0 = Genre.objects.create(name='Science Fiction')
        self.language_0 = Language.objects.create(name='English')
        self.book_0 = Book.objects.create(title='Big Book', author=self.author_0,
                                          summary='Big Summary', isbn='1234567890123',
                                          language=self.language_0)
        self.book_0.genre.set([self.genre_0])
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_book_relation = UserBookRelation.objects.create(user=self.user, book=self.book_0, status='r')

    def test_user_book_relation_create(self):
        """
        Test the user book relation
        """
        self.assertEqual(self.user_book_relation.user, self.user)
        self.assertEqual(self.user_book_relation.book, self.book_0)
        self.assertEqual(self.user_book_relation.status, 'r')

    def test_user_book_relation_str_method(self):
        """
        Test the user book relation str method
        """
        self.assertEqual(str(self.user_book_relation), 'testuser (Big Book)')

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
        self.user_book_relation.delete()
        self.assertEqual(UserBookRelation.objects.all().count(), 0)

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
            UserBookRelation.objects.create(user=self.user, book=self.book_0, status='r')
        self.assertIn("User book relation with this User and Book already exists",
                      e.exception.message_dict['__all__'][0])

#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         author = Author.objects.create(first_name='Big', last_name='Bob')
#         genre = Genre.objects.create(name='Science Fiction')
#         language = Language.objects.create(name='English')
#         book = Book.objects.create(title='Big Book', author=author, summary='Big Summary', isbn='1234567890123', language=language)
#         book.genre.set([genre])
#         saga = BookSaga.objects.create(name='Big Saga', author=Author.objects.get(id=1))

#     def test_title_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('title').verbose_name
#         self.assertEqual(field_label, 'title')

#     def test_title_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field('title').max_length
#         self.assertEqual(max_length, 200)

#     def test_author_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('author').verbose_name
#         self.assertEqual(field_label, 'author')

#     def test_summary_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('summary').verbose_name
#         self.assertEqual(field_label, 'summary')

#     def test_isbn_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('isbn').verbose_name
#         self.assertEqual(field_label, 'isbn')

#     def test_isbn_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field('isbn').max_length
#         self.assertEqual(max_length, 13)

#     def test_genre_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('genre').verbose_name
#         self.assertEqual(field_label, 'genre')

#     def test_language_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('language').verbose_name
#         self.assertEqual(field_label, 'language')

#     def test_saga_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('saga').verbose_name
#         self.assertEqual(field_label, 'saga')
    
#     def test_saga_volume(self):
#         with self.assertRaises(Exception):
#             book = Book.objects.create(title='Big Book', author=Author.objects.get(id=1), summary='Big Summary', isbn='1234567890123', language=Language.objects.get(id=1),
#                             saga=BookSaga.objects.get(id=1))

#     def test_volume_unique_in_saga(self):
#         Book.objects.create(title='Book 1', author=Author.objects.get(id=1), saga=BookSaga.objects.get(id=1), saga_volume=1, language = Language.objects.get(id=1))
#         with self.assertRaises(Exception):
#             Book.objects.create(title='Book 2', author=Author.objects.get(id=1), saga=BookSaga.objects.get(id=1), saga_volume=1, language = Language.objects.get(id=1))

#     def test_get_absolute_url(self):
#         book = Book.objects.get(id=1)
#         # This will also fail if the urlconf is not defined.
#         self.assertEqual(book.get_absolute_url(), '/book_catalog/book/1')

# class BookSagaModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         author = Author.objects.create(first_name='Big', last_name='Bob')
#         saga = BookSaga.objects.create(name='Big Saga', author=author)
#         language = Language.objects.create(name='English')
#         Book.objects.create(title='Big Book', author=author, summary='Big Summary', isbn='1234567890123', saga = saga, saga_volume = 1, language = language)
        
#     def test_name_label(self):
#         saga = BookSaga.objects.get(id=1)
#         field_label = saga._meta.get_field('name').verbose_name
#         self.assertEqual(field_label, 'name')

#     def test_name_max_length(self):
#         saga = BookSaga.objects.get(id=1)
#         max_length = saga._meta.get_field('name').max_length
#         self.assertEqual(max_length, 200)

#     def test_author_label(self):
#         saga = BookSaga.objects.get(id=1)
#         field_label = saga._meta.get_field('author').verbose_name
#         self.assertEqual(field_label, 'author')

#     def test_author_null(self):
#         saga = BookSaga.objects.get(id=1)
#         field_null = saga._meta.get_field('author').null
#         self.assertEqual(field_null, False)
    
#     def test_get_absolute_url(self):
#         saga = BookSaga.objects.get(id=1)
#         self.assertEqual(saga.get_absolute_url(), '/book_catalog/saga/1')

# class UserBookRelationModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         author = Author.objects.create(first_name='Big', last_name='Bob')
#         genre = Genre.objects.create(name='Science Fiction')
#         language = Language.objects.create(name='English')
#         book = Book.objects.create(title='Big Book', author=author, summary='Big Summary', isbn='1234567890123', language=language)
#         book.genre.set([genre])
#         saga = BookSaga.objects.create(name='Big Saga', author=Author.objects.get(id=1))
#         user = User.objects.create_user(username='testuser', password='12345')
#         test0 = UserBookRelation.objects.create(user=user, book=book, status='r')

#     def test_correct_UserBookRelation(self):
#         user = User.objects.get(id=1)
#         book = Book.objects.get(id=1)
#         user_book_relation = UserBookRelation.objects.create(user=user, book=book, status='r')
#         self.assertEqual()

#     def test_correct_choices(self):
#         user = User.objects.get(id=1)
#         book = Book.objects.get(id=1)
#         with self.assertRaises(Exception):
#             UserBookRelation.objects.create(user=user, book=book, status='l')

#     def test_user_null(self):
#         user_book_relation = UserBookRelation.objects.get(user=User.objects.get(id=1))
#         field_null = user_book_relation._meta.get_field('user').null
#         self.assertEqual(field_null, False)

#     def test_book_null(self):
#         user_book_relation = UserBookRelation.objects.get(user=User.objects.get(id=1))
#         field_null = user_book_relation._meta.get_field('book').null
#         self.assertEqual(field_null, False)

#     def test_status_null(self):
#         user_book_relation = UserBookRelation.objects.get(user=User.objects.get(id=1))
#         field_null = user_book_relation._meta.get_field('status').null
#         self.assertEqual(field_null, False)

#     def test_user_book_relation_unique(self):
#         user = User.objects.get(id=1)
#         book = Book.objects.get(id=1)
#         with self.assertRaises(Exception):
#             UserBookRelation.objects.create(user=user, book=book, status='t')
    