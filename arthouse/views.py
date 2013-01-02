from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, Http404

from django.conf import settings

# views
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView, TemplateView, DeleteView

# models
from arthouse import models

# forms
from arthouse import forms

# decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# libs
import json
import hashlib


class Home(TemplateView):
    """
    The home page for the application.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context

def login_view(request):
    """
    Allows users to log in to the system (omg!).
    """
    if request.method == 'POST':
        # authenticate the user
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'You have logged in successfully.')
                return HttpResponseRedirect(reverse('arthouse:home_url'))
            else:
                messages.add_message(request, messages.ERROR, 'Your account has been disabled. Please contact an administrator.')
        else:
            messages.add_message(request, messages.ERROR, 'Login was unsuccessful.')

        return HttpResponseRedirect(reverse('arthouse:home_url'))
    elif request.method == 'GET':
        return render(request, 'login.html', {'form': auth_forms.AuthenticationForm})
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def logout_view(request):
    """
    Allows users to log out to the system (zomgz!!1@).
    """
    logout(request)

    # Redirect to a success page.
    return HttpResponseRedirect(reverse('arthouse:home_url'))

class LoginRequiredMixin(object):
    """
    A mixin that makes sure the user is logged in before accessing the view. This
    should be the left-most mixin for a view.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        

class AccountCreateView(CreateView):
    """
    Allows registration of new user accounts.
    """
    form_class = forms.UserCreationForm
    template_name = 'accounts/create.html'
    success_url = reverse_lazy('arthouse:home_url')



class MovieDetail(DetailView):
    """

    """
    model = models.Movie
    pk_url_kwarg = 'movie_pk'
    context_object_name = 'movie'
    template_name = 'movie/detail.html'


class MovieList(ListView):
    """
    Display a list of all ``Movie``s.
    """
    model = models.Movie
    template_name = 'movie/list.html'
    context_object_name = 'movies'

    # def get_queryset(self):
    #     return self.model.objects.all()