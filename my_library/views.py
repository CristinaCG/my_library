from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic.edit import FormView
from .forms import UserRegisterForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django import forms


def not_logged_in(user):
    return not user.is_authenticated

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'auth/user_profile.html'

    def get_object(self):
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
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class UserProfileUpdateView(UpdateView):
    success_url = reverse_lazy('user_profile')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    fields = ['email', 'first_name', 'last_name']

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Type your email address'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your last name'})
        form.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your first name'})
        return form

@method_decorator(user_passes_test(not_logged_in, login_url=reverse_lazy('index')), name='dispatch')
class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'auth/user_register_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        print(user)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        form.save()
        return render(self.request, 'auth/user_register_done.html')

# class UserRegisterView(FormView):
# def user_register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             print("hello")
#             user = form.save()
#             print(user)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             messages.success(request, 'You have successfully registered')
#             return redirect('auth/user_register_form.html')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'auth/user_register_form.html', {'form': form})

# class UserChangePasswordView(LoginRequiredMixin, PasswordContextMixin,generic.UpdateView):
#     # email_template_name = "registration/password_reset_email.html"
#     # extra_email_context = None
#     form_class = PasswordChangeForm
#     html_email_template_name = None
#     subject_template_name = "registration/password_reset_subject.txt"
#     success_url = reverse_lazy("password_reset_done")
#     template_name = "registration/password_reset_form.html"
#     title = _("Password reset")
#     token_generator = default_token_generator

#     @method_decorator(csrf_protect)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         opts = {
#             "use_https": self.request.is_secure(),
#             "token_generator": self.token_generator,
#             "from_email": self.from_email,
#             "email_template_name": self.email_template_name,
#             "subject_template_name": self.subject_template_name,
#             "request": self.request,
#             "html_email_template_name": self.html_email_template_name,
#             "extra_email_context": self.extra_email_context,
#         }
#         form.save(**opts)
#         return super().form_valid(form)
    

#     model = User
#     fields = ['password']
#     login_url = '/accounts/login/'
#     redirect_field_name = 'redirect_to'
#     template_name = 'auth/user_change_password.html'
#     success_url = '/accounts/profile'

#     def get_object(self, queryset=None):
#         return self.request.user

#     def form_valid(self, form):
#         print('form_valid')
#         # Check old password
#         if not self.object.check_password(form.cleaned_data['old_password']):
#             form.add_error('old_password', 'Old password is incorrect')
#             return self.form_invalid(form)
#         # Check new password
#         if form.cleaned_data['new_password1'] != form.cleaned_data['new_password2']:
#             form.add_error('new_password2', 'Passwords do not match')
#             return self.form_invalid(form)
#         # Save new password
#         self.object = form.save(commit=False)
#         self.object.set_password(self.object.password)
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())



    