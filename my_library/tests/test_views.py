from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from my_library.forms import UserRegisterForm

class CustomLoginViewTest(TestCase):
    """
    Test custom login view.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_with_valid_credentials(self):
        """
        Test login with valid credentials.
        """
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Redirect to index
        self.assertRedirects(response, reverse('index'))

    def test_login_with_invalid_username(self):
        """
        Test login with invalid username.
        """
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This user name does not exist.')

    def test_login_with_invalid_password(self):
        """
        Test login with invalid password.
        """
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The password is not correct.')

    def test_login_form_fields(self):
        """
        Test login form fields.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsInstance(form, AuthenticationForm)
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Type your user name')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Type your password')


class UserProfileDetailViewTest(TestCase):
    """
    Test user profile detail view.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_user_profile_detail_view(self):
        """
        Test user profile detail view.
        """
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/user_profile.html')
        self.assertEqual(response.context['user'], self.user)


class UserProfileDeleteViewTest(TestCase):
    """
    Test user profile delete view.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_user_profile_delete_view(self):
        """
        Test user profile delete view.
        """
        response = self.client.post(reverse('delete_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, reverse_lazy('login'))


class UserProfileUpdateViewTest(TestCase):
    """
    Test user profile update view.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_user_profile_update_view_get(self):
        """
        Test user profile update form is displayed.
        """
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/user_form.html')
        form = response.context['form']
        self.assertEqual(form.instance, self.user)
        self.assertIn('email', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)

    def test_user_profile_update_view_post(self):
        """
        Test user profile update with valid data.
        """
        response = self.client.post(reverse('edit_profile'), {
            'email': 'newemail@example.com',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')


class UserRegisterViewTest(TestCase):
    """
    Test user registration view.
    """
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        """
        Test user registration form is displayed.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/user_register_form.html')
        form = response.context['form']
        self.assertIsInstance(form, UserRegisterForm)

    def test_register_view_post(self):
        """
        Test user registration with valid data.
        """
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'password123',
            'password_confirm': 'password123',
            'email': 'newuser@example.com',
            'first_name': 'FirstName',
            'last_name': 'LastName'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.check_password('password123'))
        self.assertTrue(new_user.is_authenticated)
        self.assertTemplateUsed(response, 'auth/user_register_done.html')