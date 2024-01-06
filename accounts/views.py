from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistration_Form, UserProfileUpdate_Form
from banking_status_app.models import BankingStatus_Model

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create your views here.
class UserRegistrationForm_View(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistration_Form
    success_url = reverse_lazy('transaction_report')

    def form_valid(self, form):
        status_check = BankingStatus_Model.objects.first()
        if status_check.banking_service:
            print(form.cleaned_data)
            new_user = form.save()
            login(self.request, new_user)
            return super().form_valid(form)         # form_valid function will be called if everything goes right.
        else:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            return super().form_invalid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserLoginForm_View(LoginView):
    template_name = 'accounts/user_login.html'
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# class UserLogoutForm_View(LogoutView):
#     print(1234)
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('home')

# class UserLogoutForm_View(LogoutView):
#     def get_success_url(self):
#         print(5678)
#         if self.request.user.is_authenticated:
#             print(1234)
#             logout(self.request)
#         return reverse_lazy('home')


# class UserLogoutForm_View(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('home')


# class UserLogoutForm_View(LogoutView):
#     next_page = reverse_lazy('home')


class UserLogoutForm_View(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserProfileUpdateForm_View(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserProfileUpdate_Form(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserProfileUpdate_Form(request.POST, instance=request.user)

        status_check = BankingStatus_Model.objects.first()
        if not status_check.banking_service:
            messages.error(self.request, 'This bank has declared bankruptcy. All services of this bank are discontinued.')
            context = {'form': form}
            return render(request, self.template_name, context)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'Your profile information has been updated successfully!')
            return redirect('update_profile')
        context = {'form': form}
        return render(request, self.template_name, context)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
