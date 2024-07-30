from django.test import TestCase
from django.contrib.auth.models import User
from my_library.forms import UserRegisterForm

class UserRegisterFormTests(TestCase):
    """
    Test user registration form.
    """
    def test_valid_form(self):
        """
        Test valid form data.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        """
        Test passwords do not match.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'password124'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', form.errors['__all__'])

    def test_missing_required_field(self):
        """
        Test missing required field.
        """
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_field_format(self):
        """
        Test email field format.
        """
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_unique_username(self):
        """
        Test unique username.
        """
        User.objects.create_user(username='testuser', password='password123')
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
