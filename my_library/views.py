from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .forms import UserRegisterForm

def not_logged_in(user):
    """
    Check if the user is not logged in.
    """
    return not user.is_authenticated

class CustomLoginView(LoginView):
    """
    Custom login view.
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    form_class = AuthenticationForm

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.filter(username=username).exists()
        if not user:
            form.add_error('username', 'This user name does not exist.')
            return super().form_invalid(form)
        user = authenticate(username=username, password=password)
        if user is None:
            form.add_error('password', 'The password is not correct.')
            return super().form_invalid(form)

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        """
        return reverse_lazy('index')

    def get_form(self, form_class=None):
        """
        Add placeholders and classes to form fields.
        """
        form = super().get_form()
        form.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your user name'})
        form.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your password'})
        return form

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Generic class-based view for displaying a user profile.
    """
    model = User
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'auth/user_profile.html'

    def get_object(self, queryset=None):
        """
        Return the user profile.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Generic class-based view for deleting a book.
    """
    model = User
    success_url = reverse_lazy('login')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'auth/user_confirm_delete.html'

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        success_url = self.get_success_url()
        obj.delete()
        return HttpResponseRedirect(success_url)

class UserProfileUpdateView(UpdateView):
    """
    Generic class-based view for updating a user profile.
    """
    success_url = reverse_lazy('user_profile')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    fields = ['email', 'first_name', 'last_name']

    def get_object(self, queryset=None):
        """
        Return the user profile.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add the user to the context.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_form(self, form_class=None):
        """
        Add placeholders and classes to form fields.
        """
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your email address'})
        form.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your last name'})
        form.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your first name'})
        return form

@method_decorator(user_passes_test(not_logged_in, login_url=reverse_lazy('index')), name='dispatch')
class UserRegisterView(FormView):
    """
    View for registering a new user.
    """
    form_class = UserRegisterForm
    template_name = 'auth/user_register_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return render(self.request, 'auth/user_register_done.html', {'user': user})
