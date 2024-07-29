from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils import timezone
from book_catalog.models import Author, Book, User, BookSaga, UserBookRelation, Genre

################# List Views #################

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

    def test_lists_all_authors(self):
        """
        Test if all authors are listed
        """
        response = self.client.get(reverse('authors')+'?page=3')
        self.assertEqual(response.status_code, 200)

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

    def test_lists_all_books(self):
        """
        Test if all books are listed
        """
        response = self.client.get(reverse('books')+'?page=3')
        self.assertEqual(response.status_code, 200)

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

################# Detail Views #################

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
        cls.relation = UserBookRelation.objects.create(user=cls.user, book=cls.book,
                                        status='r',
                                        rating=5,
                                        review='Great book',
                                        review_date='2021-01-01')

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

    def test_context_contains_correct_with_user_logged(self):
        """
        Test if context contains correct with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.get(reverse('book-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('my_book' in response.context)
        self.assertTrue('average_rating' in response.context)
        self.assertTrue('average_rating_over_100' in response.context)
        self.assertTrue('total_ratings' in response.context)
        self.assertTrue('rating_range' in response.context)
        self.assertTrue('total_reviews' in response.context)
        self.assertTrue('book_reviews' in response.context)
        self.assertEqual(response.context['my_book'], self.relation)
        self.assertEqual(response.context['average_rating'], 5)
        self.assertEqual(response.context['average_rating_over_100'], 100)
        self.assertEqual(response.context['total_ratings'], 1)
        self.assertEqual(response.context['rating_range'], range(5,0,-1))
        self.assertEqual(response.context['total_reviews'], 1)
        self.assertEqual(response.context['book_reviews'], [self.relation])
        self.assertEqual(response.context['book_reviews'][0].user.review_count, 1)
        self.assertEqual(response.context['book_reviews'][0].user.average_rating, 1)
        self.assertEqual(response.context['book_reviews'][0].rating_over_100, 100)

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
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
            saga=cls.saga,
            saga_volume=1,
        )
        cls.relation = UserBookRelation.objects.create(user=cls.user, book=cls.book,
                                                    status='r', rating=5,
                                                    review='Great book', review_date='2021-01-01')

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

    def test_context_contains_correct_with_user_logged(self):
        """
        Test if context contains correct with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('books' in response.context)
        self.assertTrue('average_rating' in response.context)
        self.assertTrue('average_rating_over_100' in response.context)
        self.assertTrue('book_list' in response.context)
        self.assertTrue('total_ratings' in response.context)
        self.assertTrue('total_reviews' in response.context)
        self.assertTrue('user_saga_relation' in response.context)
        self.assertEqual(response.context['books'][0], self.book)
        self.assertEqual(response.context['average_rating'], 5)
        self.assertEqual(response.context['average_rating_over_100'], 100)
        self.assertEqual(response.context['book_list'][0], self.book)
        self.assertEqual(response.context['total_ratings'], 1)
        self.assertEqual(response.context['total_reviews'], 1)
        self.assertEqual(response.context['user_saga_relation'], 'r')

    def test_booksaga_relation_read_with_user_logged(self):
        """
        Test if context contains correct with user logged
        """
        self.client.login(username=self.user, password='12345')
        book1 = Book.objects.get(id=1)
        book2 = Book.objects.create(
            title='The Book 2',
            author=Author.objects.get(id=1),
            saga=BookSaga.objects.get(id=1),
            saga_volume=2,
        )
        book3 = Book.objects.create(
            title='The Book 3',
            author=Author.objects.get(id=1),
            saga=BookSaga.objects.get(id=1),
            saga_volume=3,
        )
        relation1 = self.relation
        relation2 = UserBookRelation.objects.create(user=self.user, book=book2, status='t')
        relation3 = UserBookRelation.objects.create(user=self.user, book=book3, status='t')
        response = self.client.get(reverse('saga-detail', args=[1]))
        relation1.status = 't'
        relation1.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 't')
        relation1.status = 'i'
        relation1.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 't')
        relation1.status = 'r'
        relation1.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 't')
        relation2.status = 'i'
        relation2.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 'i')
        relation2.status = 'r'
        relation2.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 'i')
        relation3.status = 'i'
        relation3.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 'i')
        relation3.status = 'r'
        relation3.save()
        response = self.client.get(reverse('saga-detail', args=[1]))
        self.assertEqual(response.context['user_saga_relation'], 'r')

################# Create Views #################

class AuthorCreateViewTest(TestCase):
    """
    Test if AuthorCreateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='add_author')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='  testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/author/create/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-create'), form_data)
        self.assertEqual(response.status_code, 302)
        author = Author.objects.create(first_name='Sara', last_name='Trueman')
        self.assertEqual(author.first_name, 'Sara')
        self.assertEqual(author.last_name, 'Trueman')
        Author.objects.all().delete()

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-create'), form_data)
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.client.login(username=self.staff.username, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-create'), form_data)
        self.assertEqual(response.status_code, 302)
        author = Author.objects.get(first_name='Sara', last_name='Trueman')
        self.assertEqual(author.first_name, 'Sara')
        self.assertEqual(author.last_name, 'Trueman')

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-create'), form_data)
        self.assertEqual(response.status_code, 403)

class BookCreateViewTest(TestCase):
    """
    Test if BookCreateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='add_book')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/book/create/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-create'), form_data)
        self.assertEqual(response.status_code, 302)
        book = Book.objects.create(title='The Book', author=self.author, summary='Book summary')
        self.assertEqual(book.title, 'The Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.summary, 'Book summary')
        Book.objects.all().delete()

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-create'), form_data)
        self.assertEqual(response.status_code, 403)
    
    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        genre = Genre.objects.create(name='Test Genre')
        form_data = {
            'title': 'The Book',
            'author': self.author.pk,
            'genre': [genre.pk],
        }
        response = self.client.post(reverse('book-create'), form_data)
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get(title='The Book')
        self.assertEqual(book.title, 'The Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.summary, '')
        self.assertEqual(book.genre.first().name, 'Test Genre')
        Book.objects.all().delete()
        Genre.objects.all().delete()

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-create'), form_data)
        self.assertEqual(response.status_code, 403)

class BookSagaCreateViewTest(TestCase):
    """
    Test if BookSagaCreateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='add_booksaga')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')
    
    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/saga/create/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('saga-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get(reverse('saga-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('saga-create'), form_data)
        self.assertEqual(response.status_code, 302)
        saga = BookSaga.objects.create(name='The Saga', author=self.author)
        self.assertEqual(saga.name, 'The Saga')
        self.assertEqual(saga.author, self.author)
        BookSaga.objects.all().delete()

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('saga-create'), form_data)
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('saga-create'), form_data)
        self.assertEqual(response.status_code, 302)
        saga = BookSaga.objects.get(name='The Saga')
        self.assertEqual(saga.name, 'The Saga')
        self.assertEqual(saga.author, self.author)
        BookSaga.objects.all().delete()

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('saga-create'), form_data)
        self.assertEqual(response.status_code, 403)

    def test_get_context_data(self):
        """
        Test if get_context_data method works correctly
        """
        self.client.login(username=self.staff.username, password='12345')
        response = self.client.get(reverse('saga-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('authors' in response.context)
        self.assertEqual(len(response.context['authors']), 1)
        self.assertEqual(response.context['authors'][0], self.author)

################# Update Views #################

class AuthorUpdateViewTest(TestCase):
    """
    Test if AuthorUpdateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='change_author')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/author/1/update/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('author-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get(reverse('author-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        author = Author.objects.get(id=1)
        self.assertEqual(author.first_name, 'Sara')
        self.assertEqual(author.last_name, 'Trueman')

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        author = Author.objects.get(id=1)
        self.assertEqual(author.first_name, 'Sara')
        self.assertEqual(author.last_name, 'Trueman')

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'first_name': 'Sara', 'last_name': 'Trueman'}
        response = self.client.post(reverse('author-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

    def test_get_context_data(self):
        """
        Test if get_context_data method works correctly
        """
        book = Book.objects.create(title='The Book', author=self.author, summary='Book summary')
        self.client.login(username=self.staff.username, password='12345')
        response = self.client.get(reverse('author-update', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('books' in response.context)
        self.assertEqual(response.context['books'][0], book)

class BookUpdateViewTest(TestCase):
    """
    Test if BookUpdateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='change_book')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')
        cls.book = Book.objects.create(title='The Book', author=cls.author, summary='Book summary')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/book/1/update/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('book-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get(id=1)
        self.assertEqual(book.title, 'The Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.summary, 'Book summary')

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        genre = Genre.objects.create(name='Test Genre')
        form_data = {
            'title': 'The Book',
            'author': self.author.pk,
            'genre': [genre.pk],
        }
        response = self.client.post(reverse('book-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get(id=1)
        self.assertEqual(book.title, 'The Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.summary, '')
        self.assertEqual(book.genre.first().name, 'Test Genre')
        Genre.objects.all().delete()

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'title': 'The Book', 'author': self.author.pk, 'summary': 'Book summary'}
        response = self.client.post(reverse('book-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

class BookSagaUpdateViewTest(TestCase):
    """
    Test if BookSagaUpdateView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='change_booksaga')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')
        cls.saga = BookSaga.objects.create(name='The Saga', author=cls.author)

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/saga/1/update/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('booksaga-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('booksaga-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        saga = BookSaga.objects.get(id=1)
        self.assertEqual(saga.name, 'The Saga')
        self.assertEqual(saga.author, self.author)

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('booksaga-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('booksaga-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 302)
        saga = BookSaga.objects.get(id=1)
        self.assertEqual(saga.name, 'The Saga')
        self.assertEqual(saga.author, self.author)

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        form_data = {'name': 'The Saga', 'author': self.author.pk}
        response = self.client.post(reverse('booksaga-update', args=[1]), form_data)
        self.assertEqual(response.status_code, 403)

class UserBookRelationUpdateViewTest(TestCase):
    """
    Test if UserBookRelationUpdateView works correctly
    """
    def setUp(cls):
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
        cls.test_uuid=str(cls.user_book_relation.id)

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get(f'/book_catalog/userbookrelation/{self.test_uuid}/update/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('change-userbookrelation', args=[self.test_uuid]))
        self.assertEqual(response.status_code, 302)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        form_data = {'status': 't'}
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        self.assertEqual(response.status_code, 302)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.status, 'r')

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'status': 't'}
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_not_existing_relation(self):
        """
        Test if view redirects for not existing relation
        """
        response = self.client.get(reverse('change-userbookrelation', args=[self.test_uuid]))
        self.assertEqual(response.status_code, 302)

    def test_view_update_status(self):
        """
        Test if view updates status correctly
        """
        self.client.login(username=self.user, password='12345')
        form_data = {'status': 't'}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.status, 'r')
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.status, 't')
        form_data = {'status': 'i'}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.status, 'i')
        self.assertEqual(relation.reading_date, timezone.now().date())
        form_data = {'status': 'r'}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.status, 'r')
        self.assertEqual(relation.read_date, timezone.now().date())

    def test_view_update_review(self):
        """
        Test if view updates review correctly
        """
        self.client.login(username=self.user.username, password='12345')
        form_data = {'review': 'Great book'}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.review, None)
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.review, 'Great book')
        self.assertEqual(relation.review_date, timezone.now().date())

    def test_view_update_rating(self):
        """
        Test if view updates rating correctly
        """
        self.client.login(username=self.user.username, password='12345')
        form_data = {'rating': 5}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.rating, None)
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.rating, 5)
        form_data = {'rating': 3}
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        response = self.client.post(reverse('change-userbookrelation', args=[self.test_uuid]), form_data)
        relation = UserBookRelation.objects.get(id=self.test_uuid)
        self.assertEqual(relation.rating, 3)

################# Delete Views #################

class AuthorDeleteViewTest(TestCase):
    """
    Test if AuthorDeleteView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='delete_author')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/author/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), 1)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('author-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), 1)

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.post(reverse('author-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        response = self.client.post(reverse('author-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), 0)

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        response = self.client.post(reverse('author-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

class BookDeleteViewTest(TestCase):
    """
    Test if BookDeleteView works correctly
    """
    @classmethod 
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='delete_book')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')
        cls.book = Book.objects.create(title='The Book', author=cls.author, summary='Book summary')

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/book/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('book-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.post(reverse('book-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        response = self.client.post(reverse('book-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        
        self.client.login(username=self.user.username, password='12345')
        response = self.client.post(reverse('book-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

class BookSagaDeleteViewTest(TestCase):
    """
    Test if BookSagaDeleteView works correctly
    """
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(username='staffuser', password='12345')
        cls.permission = Permission.objects.get(codename='delete_booksaga')
        cls.staff.user_permissions.add(cls.permission)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(first_name='Sara', last_name='Trueman')
        cls.saga = BookSaga.objects.create(name='The Saga', author=cls.author)

    def test_view_url_exists_at_desired_location(self):
        """
        Test if view is accessible
        """
        response = self.client.get('/book_catalog/saga/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookSaga.objects.count(), 1)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('booksaga-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookSaga.objects.count(), 1)

    def test_view_method_post_with_user_logged(self):
        """
        Test if view method is POST with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.post(reverse('booksaga-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_view_post_with_permission(self):
        """
        Test if view method is POST with user logged and has permission
        """
        self.staff.user_permissions.add(self.permission)
        self.client.login(username=self.staff.username, password='12345')
        response = self.client.post(reverse('booksaga-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookSaga.objects.count(), 0)

    def test_view_post_without_permission(self):
        """
        Test if view method is POST with user logged but without permission
        """
        # Remove permission
        self.user.user_permissions.remove(self.permission)
        self.client.login(username=self.user.username, password='12345')
        response = self.client.post(reverse('booksaga-delete', args=[1]))
        self.assertEqual(response.status_code, 403)

class SearchViewTest(TestCase):
    """
    Test if SearchView works correctly
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.author1 = Author.objects.create(first_name='John', last_name='Doe')
        self.author2 = Author.objects.create(first_name='Jane', last_name='Smith')
        self.saga = BookSaga.objects.create(name='Epic Saga',author=self.author1)
        self.book1 = Book.objects.create(title='Great', author=self.author1)
        self.book2 = Book.objects.create(title='Another Great', author=self.author2)
        self.book3 = Book.objects.create(title='Saga', author=self.author1,saga=self.saga,
                                         saga_volume=1)
        self.user_book_relation = UserBookRelation.objects.create(user=self.user, book=self.book1, status='r')

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        response = self.client.get(reverse('search'), {'query': 'Great'})
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        response = self.client.get(reverse('search'), {'query': 'Great'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

    def test_context_contains_correct_search_results(self):
        """
        Test if context contains correct search results
        """
        response = self.client.get(reverse('search'), {'query': 'Great'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 2)
        self.assertEqual(response.context['book_results'][0], self.book2)
        self.assertEqual(response.context['book_results'][1], self.book1)

    def test_context_contains_correct_search_results_with_no_books(self):
        """
        Test if context contains correct search results with no books
        """
        response = self.client.get(reverse('search'), {'query': 'Book'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 0)

    def test_context_contains_correct_search_results_with_no_query(self):
        """
        Test if context contains correct search results with no query
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 3)

    def test_context_contains_correct_search_results_with_user_logged(self):
        """
        Test if context contains correct search results with user logged
        """
        response = self.client.get(reverse('search'), {'query': 'Saga'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(response.context['book_results'][0], self.book3)

    def test_context_contains_correct_search_results_with_no_books_and_user_logged(self):
        """
        Test if context contains correct search results with no books and user logged
        """
        Book.objects.all().delete()
        response = self.client.get(reverse('search'), {'query': 'Saga'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 0)

    def test_context_contains_correct_search_results_with_no_query_and_user_logged(self):
        """
        Test if context contains correct search results with no query and user logged
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 3)

    def test_context_contains_correct_search_results_with_no_books_and_no_query_and_user_logged(self):
        """
        Test if context contains correct search results with no books and no query and user logged
        """
        Book.objects.all().delete()
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 0)

    def test_context_contains_correct_search_results_with_no_books_and_no_query_and_no_user_logged(self):
        """
        Test if context contains correct search results with no books and no query and no user logged
        """
        Book.objects.all().delete()
        self.client.logout()
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 0)

    def test_search_by_title(self):
        """
        Test if search by title works correctly
        """
        response = self.client.get(reverse('search'), {'query': 'Great'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 2)
        self.assertEqual(response.context['book_results'][0], self.book2)
        self.assertEqual(response.context['book_results'][1], self.book1)
    
    def test_search_by_author(self):
        """
        Test if search by author works correctly
        """
        response = self.client.get(reverse('search'), {'query': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 2)
        self.assertEqual(response.context['book_results'][0], self.book1)
        self.assertEqual(response.context['book_results'][1], self.book3)

    def test_search_by_saga(self):
        """
        Test if search by saga works correctly
        """
        response = self.client.get(reverse('search'), {'query': 'Epic'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('book_results' in response.context)
        self.assertEqual(len(response.context['book_results']), 1)
        self.assertEqual(response.context['book_results'][0], self.book3)

################# General Views #################

class ChangeBookStatusViewTest(TestCase):
    """
    Test if ChangeBookStatusView works correctly
    """
    def setUp(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.author = Author.objects.create(
            first_name='Sara',
            last_name='Trueman',
        )
        cls.book = Book.objects.create(
            title='The Book',
            author=cls.author,
            summary='Book summary',
        )
        cls.user_book_relation = UserBookRelation.objects.create(
                user=cls.user,
                book=cls.book,
                status='t',
            )

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        UserBookRelation.objects.all().delete()

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/book/'+str(self.book.pk)+'/change-status/t/')
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-book-status', args=[2,'t']))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('change-book-status', args=[2,'t']))
        self.assertNotEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 't']))
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get('/book_catalog/book/'+str(self.book.pk)+'/change-status/d/')
        self.assertEqual(response.status_code, 302)

    def test_user_with_no_relation(self):
        """
        Test if user with no relation works correctly
        """
        UserBookRelation.objects.all().delete()
        self.client.login(username=self.user.username, password='12345')
        relation = UserBookRelation.objects.filter(user=self.user, book=self.book).first()
        self.assertEqual(relation, None)
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 't']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 't')
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'i']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'i')
        self.assertEqual(relation.reading_date, timezone.now().date())
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'r']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'r')
        self.assertEqual(relation.read_date, timezone.now().date())

    def test_user_with_relation(self):
        """
        Test if user with no relation works correctly
        """
        self.client.login(username=self.user.username, password='12345')
        relation = UserBookRelation.objects.filter(user=self.user, book=self.book).first()
        self.assertNotEqual(relation, None)
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 't']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 't')
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'i']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'i')
        self.assertEqual(relation.reading_date, timezone.now().date())
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'r']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'r')
        self.assertEqual(relation.read_date, timezone.now().date())

    def test_user_without_relation_status_i(self):
        """
        Test if user without relation works correctly
        """
        UserBookRelation.objects.all().delete()
        self.client.login(username=self.user.username, password='12345')
        relation = UserBookRelation.objects.filter(user=self.user, book=self.book).first()
        self.assertEqual(relation, None)
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'i']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'i')
        self.assertEqual(relation.reading_date, timezone.now().date())

    def test_user_without_relation_status_r(self):
        """
        Test if user without relation works correctly
        """
        UserBookRelation.objects.all().delete()
        self.client.login(username=self.user.username, password='12345')
        relation = UserBookRelation.objects.filter(user=self.user, book=self.book).first()
        self.assertEqual(relation, None)
        response = self.client.get(reverse('change-book-status', args=[self.book.pk, 'r']))
        relation = UserBookRelation.objects.filter(user=self.user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 'r')
        self.assertEqual(relation.read_date, timezone.now().date())

class ChangeBookSagaStatusViewTest(TestCase):
    """
    Test if ChangeBookSagaStatusView works correctly
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
        cls.book = Book.objects.create(
            title='The Book',
            author=author,
            summary='Book summary',
            saga=cls.saga,
            saga_volume=1,
        )
        cls.relation = UserBookRelation.objects.create(user=cls.user, book=cls.book,
                                                    status='r', rating=5,
                                                    review='Great book', review_date='2021-01-01')

    def test_view_url_redirects_for_anonymous_user(self):
        """
        Test if view redirects an anonymous user
        """
        response = self.client.get('/book_catalog/saga/1/change-status/r/')
        self.assertNotEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """ 
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-booksaga-status', args=[1,'r']))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-booksaga-status', args=[2,'r']))
        self.assertNotEqual(response.status_code, 200)

    def test_view_redirects_for_not_existing_book_for_anonymous_user(self):
        """
        Test if view redirects for not existing book for anonymous user
        """
        response = self.client.get(reverse('change-booksaga-status', args=[2,'r']))
        self.assertNotEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if view uses correct template
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('change-booksaga-status', args=[1, 'r']))
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location_for_logged_in_user(self):
        """
        Test if view is accessible only for logged-in user
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/book_catalog/saga/1/change-status/d/')
        self.assertEqual(response.status_code, 302)

    def test_user_with_no_relation(self):
        """
        Test if user with no relation works correctly
        """
        user = User.objects.create_user(username='testuser2', password='12345')
        self.client.login(username=user.username, password='12345')
        relation = UserBookRelation.objects.filter(user = user, book = self.book).first() 
        self.assertEqual(relation, None)
        response = self.client.get(reverse('change-booksaga-status', args=[1, 't']))
        relation = UserBookRelation.objects.filter(user = user, book = self.book).first()
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.status, 't')

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
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.relation = UserBookRelation.objects.create(
            user=cls.user,
            book=Book.objects.get(id=1),
            status='r',
        )

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
        self.assertTrue('total_books' in response.context)
        self.assertTrue('total_authors' in response.context)
        self.assertTrue('recent_books' in response.context)
        self.assertEqual(response.context['total_books'], 5)
        self.assertEqual(response.context['total_authors'], 3)
        self.assertEqual(len(response.context['recent_books']), 5)

    def test_context_contains_correct_book_and_author_counts_with_no_books(self):
        """
        Test if context contains correct book and author counts with no books
        """
        Book.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total_books' in response.context)
        self.assertTrue('total_authors' in response.context)
        self.assertTrue('recent_books' in response.context)
        self.assertEqual(response.context['total_books'], 0)
        self.assertEqual(response.context['total_authors'], 3)
        self.assertEqual(len(response.context['recent_books']), 0)

    def test_context_contains_correct_book_and_author_counts_with_no_authors(self):
        """
        Test if context contains correct book and author counts with no authors
        """
        Author.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total_books' in response.context)
        self.assertTrue('total_authors' in response.context)
        self.assertTrue('recent_books' in response.context)
        self.assertEqual(response.context['total_books'], 0)
        self.assertEqual(response.context['total_authors'], 0)
        self.assertEqual(len(response.context['recent_books']), 0)

    def test_context_contains_correct_book_and_author_counts_with_no_books_and_no_authors(self):
        """
        Test if context contains correct book and author counts with no books and no authors
        """
        Book.objects.all().delete()
        Author.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total_books' in response.context)
        self.assertTrue('total_authors' in response.context)
        self.assertTrue('recent_books' in response.context)
        self.assertEqual(response.context['total_books'], 0)
        self.assertEqual(response.context['total_authors'], 0)
        self.assertEqual(len(response.context['recent_books']), 0)

    def test_context_contains_correct_with_user_logged(self):
        """
        Test if context contains correct with user logged
        """
        self.client.login(username=self.user, password='12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('my_books_reading' in response.context)
        self.assertTrue('my_books_read' in response.context)
        self.assertTrue('my_books_this_year' in response.context)
        self.assertEqual(response.context['my_books_reading'], [])
        self.assertEqual(response.context['my_books_read'], 1)
        self.assertEqual(response.context['my_books_this_year'], 1)

class RatingBookViewTest(TestCase):
    """
    Test if RatingBookView works correctly
    """
    def setUp(cls):
        super().setUp()
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
        cls.relation = UserBookRelation.objects.create(
            user=cls.user,
            book=cls.book,
            status='r',
        )

    def tearDown(self):
        super().tearDown()
        User.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        UserBookRelation.objects.all().delete()

    def test_view_url_accessible_by_name(self):
        """
        Test if view is accessible by name
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('rating-book', args=[1, 2]))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_for_not_existing_book(self):
        """
        Test if view redirects for not existing book
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('rating-book', args=[3, 2]))
        self.assertNotEqual(response.status_code, 200)

    def test_view_method_post(self):
        """
        Test if view method is POST
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('rating-book', args=[self.book.pk, 2]))
        self.assertRedirects(response, reverse('book-detail', args=[self.book.pk]))
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertEqual(relation.rating, 2)

    def test_view_delete_rating(self):
        """
        Test if view method is POST
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('rating-book', args=[self.book.pk, 2]))
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertEqual(relation.rating, 2)
        response = self.client.post(reverse('rating-book', args=[self.book.pk, 2]))
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertEqual(relation.rating, None)

    def test_view_without_relation(self):
        """
        Test if view method is POST
        """
        self.client.login(username='testuser', password='12345')
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        relation.delete()
        relation = UserBookRelation.objects.filter(user=self.user).first()
        self.assertEqual(relation, None)
        response = self.client.post(reverse('rating-book', args=[self.book.pk, 2]))
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertNotEqual(relation, None)
        self.assertEqual(relation.rating, 2)
