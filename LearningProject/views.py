from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from LearningProject.forms import RegistrationForm, UsageForm, EditProfileForm
from LearningProject.models import Usage
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
import re
import json
from django.contrib.auth.models import User

###### BADGES ######
from pinax.badges.base import Badge, BadgeAwarded, BadgeDetail
from pinax.badges.registry import badges


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
    try:
        usagedata = Usage.objects.get(user=request.user)
        args = {'user': request.user, 'usagedata':usagedata}
        return render(request, "webapp/profile.html", args)
    except:
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
    # return same data as in data1, but in object form. Used for saving variables to model & database
    usagedata = Usage.objects.get(user=request.user)

    # retrieve cost value from Usage model for signed in user, store in cost variable
    for c in data1:
        elec_cost = c.elec_cost
        gas_cost = c.gas_cost
        oil_cost = c.oil_cost
        standingC = c.standing_charge
        county = c.county
        if county == '':
            county = 'your county'

        gas = c.gas
        electricity = c.electricity
        oil = c.oil
        oilfreq = c.oil_frequency

    # for loop iterates through data1 to check stored value for current month, assigns to 'data2'
    # data2 stores integer value of current month energy usage from Usage model
    # data3 stores integer value of previous month, used for progress checks and comparisons later
    for m in data1:
        janData = m.Jan
        febData = m.Feb
        marData = m.Mar
        aprData = m.Apr

        if thismonth == 'Jan':
            data2 = m.Jan
        elif thismonth == 'Feb':
            data2 = m.Feb
        elif thismonth == 'Apr':
            data2 = m.Apr
            data3 = m.Mar

            oil2 = m.Apr_oil
            gas2 = m.Apr_gas
            elec2 = m.Apr_elec

            oil3 = m.Mar_oil
            gas3 = m.Mar_gas
            elec3 = m.Mar_elec

        # set empty value for arg variables to avoid error when not populated due to later defined conditional blocks

        difference = ''
        percentage_change = 0
        savings = 0
        elec_cost = elec_cost - standingC

        class GreenTestBadge(Badge):
            slug = "testbadge"
            levels = [
                "Achieved"
            ]
            events = [
                "testbadge_awarded"
            ]
            multiple = False

            def award(self, **state):
                user = state["user"]
                if usagedata.greenmonth is True:
                    return BadgeAwarded(level=1)

        badges.register(GreenTestBadge)

        # evaluating comparison of data1 and data2, storing result in progress_check and setting greenmonth status
        if data2 < data3:
            if data2 != 0 and data3 != 0:
                progress_check = 'Congratulations on a Green ' + thismonth_full + '!'
                greenmonth = True
                usagedata.greenmonth = True
                badges.possibly_award_badge("testbadge_awarded", user=request.user)

                # calculate difference between last month and previous month, calculate % change in consumption
                # calculate per unit rate of consumption, calculate savings based on unit rate and change in consumption

                elec_diff = elec3 - elec2
                if elec_cost == 0:
                    elec_rate = 0
                else:
                    elec_rate = elec_cost / elec2
                elec_savings = int(elec_rate * elec_diff)

                oil_diff = oil3 - oil2
                if oil_cost == 0:
                    oil_rate = 0
                else:
                    oil_rate = oil_cost / oil2
                oil_savings = int(oil_rate * oil_diff)

                gas_diff = gas3 - gas2
                if gas_cost == 0:
                    gas_rate = 0
                else:
                    gas_rate = gas_cost / gas2
                gas_savings = int(gas_rate * gas_diff)

                difference = data3 - data2
                savings = (gas_savings + oil_savings + elec_savings)

                usagedata.difference = difference  # update usagedata object
                percentage_change = int(difference / data3 * 100)
                usagedata.reduction_percentage = percentage_change
                usagedata.save()  # save updated object to database / Usage model

                # savings = int(rate * difference)
                args = {'data1': data1,
                        'lastmonth': lastmonth, 'thismonth': thismonth, 'thismonth_full':thismonth_full,
                        'county': county, 'greenmonth': greenmonth,
                        'data2': data2, 'data3': data3,
                        'progress_check': progress_check,
                        'difference': difference, 'percentage_change': percentage_change,
                        'savings': savings, 'standingC': standingC,
                        'janData': janData, 'febData': febData, 'marData': marData, 'aprData': aprData,
                        'gas_savings': gas_savings, 'elec_savings': elec_savings, 'oil_savings': oil_savings}
                return render(request, "webapp/feedback.html", args)

        elif data2 > data3:
            if data2 != 0 and data3 != 0:
                progress_check = 'You did not reduce your energy use in ' + thismonth_full + '.'
                greenmonth = False

                elec_diff = elec2 - elec3
                if elec_cost == 0:
                    elec_rate =0
                else:
                    elec_rate = elec_cost / elec2
                elec_savings = int(elec_rate * elec_diff)

                oil_diff = oil2 - oil3
                if oil_cost ==0:
                    oil_rate =0
                else:
                    oil_rate = oil_cost / oil2
                oil_savings = int(oil_rate * oil_diff)

                gas_diff = gas2 - gas3
                if gas_cost == 0:
                    gas_rate =0
                else:
                    gas_rate = gas_cost / gas2
                gas_savings = int(gas_rate * gas_diff)

                difference = data2 - data3
                percentage_change = int(difference / data2 * 100)
                usagedata.difference = difference  # update usagedata object
                usagedata.reduction_percentage = 0
                usagedata.save()  # save updated object to database / Usage model

                savings = (gas_savings + oil_savings + elec_savings)

                args = {'data1': data1,
                        'lastmonth': lastmonth, 'thismonth': thismonth, 'county': county,
                        'data2': data2, 'data3': data3,
                        'progress_check': progress_check, 'greenmonth': greenmonth,
                        'difference': difference, 'percentage_change': percentage_change,
                        'savings': savings, 'standingC': standingC,
                        'janData': janData, 'febData': febData, 'marData': marData, 'aprData': aprData}
                return render(request, "webapp/feedback.html", args)

        if data2 == 0:
            return render(request, 'webapp/stop_catchers/no-usage.html')
        if data3 == 0 and data2 != 0:
            return render(request, 'webapp/stop_catchers/first-month.html')
        if data3 == 0:
            return HttpResponse('')


@login_required
def monthly_use(request):
    user = request.user
    # tries to instantiate Usage model data for signed in user
    today = datetime.now()
    thismonth = today.strftime('%m')
    thismonth_full = today.strftime('%B')
    try:
        usagedata = Usage.objects.get(user_id=user)
        # code block to check current month and set data2 to represent model data for current month, then used to
        # conditionally render form to user, or tell them they have already entered this months usage
        data1 = Usage.objects.filter(user=request.user)
        for m in data1:
            if thismonth == '01':
                data2 = m.Jan
            elif thismonth == '02':
                data2 = m.Feb
            elif thismonth == '04':
                data2 = m.Apr

        for c in data1:
            county = c.county

        if data2 == 0:
            if request.method == 'POST':
                # instance enables updating of database values from fresh form / model variables
                # difference = data3 - data2
                form = UsageForm(request.POST, instance=usagedata)
                if form.is_valid():
                    usage = form.save(commit=False)
                    if thismonth == '04':
                        if usage.Apr_oil != 0:
                            if usage.oil_frequency != 0:
                                usage.Apr_oil = (usage.Apr_oil * 10.35) / usage.oil_frequency
                        usage.Apr = usagedata.Apr_gas + usagedata.Apr_elec + usagedata.Apr_oil
                        usage.user = request.user
                        usage.save()
                return redirect('/webapp/feedback')
            else:
                form = UsageForm(instance=request.user)
                # check current month, used later at template level to render only the form field of current month
                thismonth = datetime.now().strftime('%m')

                # check if user has entered a county already, used in template for conditional render of form
                if county == '':
                    enter_county = True
                else:
                    enter_county = False

                args = {'form': form, 'thismonth': thismonth, 'thismonth_full': thismonth_full,
                        'enter_county': enter_county}
                return render(request, 'webapp/monthly_use_form.html', args)
        else:
            return render(request, 'webapp/stop_catchers/already-entered.html')

    # catches exception for new users without pre-existing data in the Usage model, creates new database entry
    # for signed in user ID.
    except ObjectDoesNotExist:
        if request.method == 'POST':
            # instance enables updating of database values from fresh form / model variables
            form = UsageForm(request.POST)
            if form.is_valid():
                usage = form.save(commit=False)
                usage.user = request.user
                usage.save()
            return redirect('/webapp/feedback')
        else:
            form = UsageForm(instance=request.user)
            # check current month, used later at template level to render only the form field of current month
            thismonth = datetime.now().strftime('%m')
            args = {'form': form, 'thismonth': thismonth, 'thismonth_full': thismonth_full}
            return render(request, 'webapp/monthly_use_form.html', args)


@login_required
def comparative_feedback(request):
    user = request.user
    today = datetime.now()
    thismonth_full = today.strftime('%B')

    usagedata = Usage.objects.filter(user=request.user)
    for c in usagedata:
        county = c.county
        reduction = c.reduction_percentage
        data2 = c.Apr

    data1 = Usage.objects.filter(county=county)
    for m in data1:
        Apr = m.Apr

    if data2 != 0:
        comparative_leaderboard = data1.order_by('-reduction_percentage')[:10]
        ranking = Usage.objects.filter(user__usage__reduction_percentage__gte=reduction).count()

        # # if rankingdata ==1:
        # #     ranking = 1
        # # else:
        # #     ranking = rankingdata -1
        #
        # ranking = rankingdata -1
    else:
        comparative_leaderboard = data1.order_by('-reduction_percentage')[:10]
        ranking = 'n/a'

    countydata = Usage.objects.filter(user__usage__county=county).values('Apr', 'user_id')
    countyavg = countydata.aggregate(Avg('Apr'))
    countyavgReductiondata = Usage.objects.filter(user__usage__county=county).values('reduction_percentage')
    countyavgReduction = countyavgReductiondata.aggregate(Avg('reduction_percentage'))

    count_values = countydata.count()
    if count_values:
        percentile = int((data1.filter(reduction_percentage__gte=reduction).count()) / count_values * 100)
    else:
        return 0.0


    roundrank = 5 * round(percentile/5)

    betterThan = 100 - percentile

    test = Usage.objects.all()

    args = {'countydata': countydata, 'countyavg': countyavg, 'percentile': percentile,'roundrank':roundrank,
            'Apr': Apr, 'county': county, 'betterThan': betterThan,
            'thismonth_full': thismonth_full, 'data2': data2,
            'countyavgReduction': countyavgReduction, 'reduction': reduction, 'user': user,
            'comparative_leaderboard': comparative_leaderboard, 'ranking': ranking, 'test': test}
    return render(request, 'webapp/comparative_feedback.html', args)

    if data2 == 0:
        return render(request, 'webapp/stop_catchers/no-usage.html')

@login_required
def view_user_profile(request, username):
    usageUserdata = User.objects.filter(username=username).only('id')
    for n in usageUserdata:
        usageUser = n.id
    usagedata = Usage.objects.filter(user_id=usageUser)
    user_profile = User.objects.get(username=username)
    args = {'user_profile': user_profile, 'usageUser': usageUser, 'usagedata': usagedata}
    return render(request, 'webapp/viewprofile.html', args)


@login_required
def group_feedback(request):
    return render(request, 'webapp/group_feedback.html')
