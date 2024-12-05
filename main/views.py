from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:index')

    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'registration/register.html', context)

def is_admin_user(user):
    return user.is_staff

@login_required
def admin_only_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, "admin_only.html")