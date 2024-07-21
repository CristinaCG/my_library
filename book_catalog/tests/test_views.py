from django.test import TestCase
# from book_catalog.views import 
from book_catalog.models import Author, Book, User, BookSaga, UserBookRelation
from django.urls import reverse


class AuthorListViewTest(TestCase):
    """
    Test if AuthorListView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 25
        for author_num in range(number_of_authors):
            Author.objects.create(
                first_name=f'Sara {author_num}',
                last_name=f'Trueman {author_num}',
            )

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/author_list.html')

    def test_pagination_is_ten(self):
        """
        Test if pagination is ten
        """
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        """
        Test if all authors are listed
        """
        response = self.client.get(reverse('authors')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 5)

class BookListViewTest(TestCase):
    """
    Test if BookListView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        number_of_books = 25
        for book_num in range(number_of_books):
            Book.objects.create(
                title=f'The Book {book_num}',
                author=Author.objects.create(first_name=f'Sara {book_num}', last_name=f'Trueman {book_num}'),
                summary=f'Book {book_num} summary',
            )

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/book_list.html')

    def test_pagination_is_ten(self):
        """
        Test if pagination is ten
        """
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 10)

    def test_lists_all_books(self):
        """
        Test if all books are listed
        """
        response = self.client.get(reverse('books')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 5)

class AuthorDetailViewTest(TestCase):
    """
    Test if AuthorDetailView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        number_of_books = 25
        for book_num in range(number_of_books):
            Book.objects.create(
                title=f'The Book {book_num}',
                author=author,
                summary=f'Book {book_num} summary',
            )
        author_2 = Author.objects.create(
            first_name='John',
            last_name='Doe',
        )
        number_of_books = 10
        for book_num in range(number_of_books):
            Book.objects.create(
                title=f'The Book {book_num}',
                author=author_2,
                summary=f'Book {book_num} summary',
            )

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/author/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/author/1')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('author-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('author-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/author_detail.html')

    def test_lists_all_books(self):
        """
        Test if all books are listed
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('author-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('books' in response.context)
        self.assertTrue(len(response.context['books']) == 25)

class BookDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
        )

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/book/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/book/1')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/book_detail.html')

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('book-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_logged_in_user(self):
        """
        Test if view redirects for not existing book for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

class BookSagaDetailViewTest(TestCase):
    """
    Test if BookSagaDetailView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        cls.saga = BookSaga.objects.create(
            name='The Saga',
            author=author,
        )

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/saga/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/saga/1')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/booksaga_detail.html')

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('saga-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('saga-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_logged_in_user(self):
        """
        Test if view redirects for not existing book for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('saga-detail', args=[2]))
        self.assertNotEqual(response.status_code, 200)

class UserBookRelationListViewTest(TestCase):
    """
    Test if UserBookRelationListView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        num_of_books = 4
        for n in range(num_of_books):
            Book.objects.create(
                title=f'The Book {n}',
                author=author,
                summary=f'Book {n} summary',
            )
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
        )
        cls.user_book_relation = UserBookRelation.objects.create(
                user=cls.user,
                book=cls.book,
                status='r',
            )

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/mybooks/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/mybooks/')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my-books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my-books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/userbookrelation_list.html')

    def test_lists_all_books(self):
        """
        Test if all books are listed
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my-books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('userbookrelation_list' in response.context)
        self.assertTrue(len(response.context['userbookrelation_list']) == 1)

class ChangeBookStatusViewTest(TestCase):
    """
    Test if ChangeBookStatusView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
        )
        cls.user_book_relation = UserBookRelation.objects.create(
                user=cls.user,
                book=cls.book,
                status='r',
            )


    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/book/1/change-status/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/book/1/change-status/')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-book-status', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-book-status', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('change-book-status', args=[2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-book-status', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_catalog/change_book_status_form.html')

    def test_view_method_post(self):
        self.client.login(username='testuser', password='12345')
        form_data = {'status': 't'}
        response = self.client.post(reverse('change-book-status', args=[self.book.pk]), form_data)
        self.assertRedirects(response, reverse('book-detail', args=[self.book.pk]))
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertEqual(relation.status, 't')

class DeleteBookStatusViewTest(TestCase):
    """
    Test if DeleteBookStatusView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
        )
        cls.user_book_relation = UserBookRelation.objects.create(
                user=cls.user,
                book=cls.book,
                status='r',
            )

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/book/1/delete-status/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/book/1/delete-status/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete-book-status', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete-book-status', args=[2]))
        self.assertNotEqual(response.status_code, 302)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('delete-book-status', args=[2]))
        self.assertEqual(response.status_code, 302)

class IndexViewTest(TestCase):
    """
    Test if index view works correctly
    """
    @classmethod
    def setUpTestData(cls):
        number_of_books = 5
        number_of_authors = 3

        for author_id in range(number_of_authors):
            Author.objects.create(first_name=f'Author {author_id}', last_name='Test')
        for book_id in range(number_of_books):
            Book.objects.create(title=f'Book {book_id}',
                                author=Author.objects.get(id=book_id % number_of_authors+1),
                                summary='Test Book')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index_book.html')

    def test_context_contains_correct_book_and_author_counts(self):
        """
        Test if context contains correct book and author counts
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_books' in response.context)
        self.assertTrue('num_authors' in response.context)
        self.assertEqual(response.context['num_books'], 5)
        self.assertEqual(response.context['num_authors'], 3)