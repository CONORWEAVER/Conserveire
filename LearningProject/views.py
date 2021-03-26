from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from LearningProject.forms import RegistrationForm, UsageForm, EditProfileForm
from LearningProject.models import Usage
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Avg
from django.contrib.auth.models import User


# Create your views here.


def home(request):
    return render(request, 'webapp/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/webapp/profile/')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'webapp/reg_form.html', args)


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, "webapp/profile.html", args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/webapp/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'webapp/edit_profile.html', args)


@login_required
def view_feedback(request):
    data1 = Usage.objects.filter(user=request.user)
    context = {
        'data1': data1
    }
    return render(request, "webapp/feedback.html", context)


@login_required
def monthly_use(request):
    user = request.user
    # instantiate Usage model data for signed in user
    usagedata = Usage.objects.get(user_id=user)
    if request.method == 'POST':
        # instance enables updating of database values from fresh form / model variables
        form = UsageForm(request.POST, instance=usagedata)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.user = request.user
            usage.save()
            return redirect('/webapp/feedback')
    else:
        form = UsageForm(instance=request.user)
        # check current month, used later at template level to render only the form field of current month
        thismonth = datetime.now().strftime('%m')
        args = {'form': form, 'thismonth': thismonth}
        return render(request, 'webapp/monthly_use_form.html', args)

# function to check date

# def checkdate():
#     thismonth = datetime.now().strftime('%m')
#     return thismonth
