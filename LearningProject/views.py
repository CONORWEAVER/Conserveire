from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from LearningProject.forms import RegistrationForm, UsageForm, EditProfileForm
from LearningProject.models import Usage
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
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
    # logic to identify current month and last month, returning string in abbreviated month format for each variable
    today = datetime.now()
    thismonth = today.strftime('%b')
    thismonth_full = today.strftime('%B')
    calcprev = today.replace(day=1) - timedelta(days=1)
    lastmonth = calcprev.strftime('%b')

    # data1 holds queryset of Usage model containing data for currently signed in user
    data1 = Usage.objects.filter(user=request.user)

    # for loop iterates through data1 to check stored value for current month, assigns to 'data2'
    # data2 stores integer value of current month energy usage from Usage model
    # data3 stores integer value of previous month, used for progress checks and comparisons later
    for m in data1:
        if thismonth == 'Jan':
            data2 = m.Jan
        elif thismonth == 'Feb':
            data2 = m.Feb
        elif thismonth == 'Apr':
            data2 = m.Apr
            data3 = m.Mar

        if data2 < data3:
            progress_check = 'Congratulations on a Green ' + thismonth_full + '!'
            greenmonth = True
        elif data2 > data3:
            progress_check = 'You did not reduce your energy use in ' + thismonth_full + '.'
            greenmonth = False

        if greenmonth:
            difference = data3 - data2
            percentage_change = int(difference / data3 * 100)


        else:
            difference = data2 - data3
            percentage_change = int(difference / data2 * 100)





    args = {'data1': data1,
            'lastmonth': lastmonth, 'thismonth': thismonth,
            'data2': data2, 'data3': data3,
            'progress_check': progress_check, 'greenmonth': greenmonth,
            'difference': difference, 'percentage_change': percentage_change}
    return render(request, "webapp/feedback.html", args)


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
