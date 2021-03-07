from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from LearningProject.forms import RegistrationForm, UsageForm
from LearningProject.models import Usage
from django.contrib.auth.models import User


# Create your views here.


def home(request):
    numbers = [1, 2, 3, 4, 5]
    name = 'Conor Weav'

    args = {'myName': name, 'numbers': numbers}
    return render(request, 'webapp/home.html', args)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/webapp/profile')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'webapp/reg_form.html', args)


def view_profile(request):
    args = {'user': request.user}
    return render(request, "webapp/profile.html", args)


def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/webapp/profile')

    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'webapp/edit_profile.html', args)


def view_feedback(request):
    return render(request, "webapp/feedback.html")

def monthly_use(request):
    if request.method == 'POST':
        form = UsageForm(request.POST, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/webapp/feedback')
    else:
        form = UsageForm(instance=request.user)
        args = {'form': form}
        return render(request, 'webapp/monthly_use_form.html', args)


