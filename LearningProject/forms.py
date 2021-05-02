from django import forms
from django.forms import ModelForm, DateInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from LearningProject.models import Usage, UserProfile, energyPledge


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class UserCountyForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('county',)


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


class UsageForm(ModelForm):
    class Meta:
        model = Usage
        fields = [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'county',
                  'cost', 'standing_charge', 'oil', 'oil_frequency', 'gas', 'electricity',
                  'elec_cost', 'gas_cost', 'oil_cost', 'Apr_elec', 'Apr_oil', 'Apr_gas',
                    'May_elec', 'May_gas', 'May_oil', 'Jun_elec', 'Jun_oil', 'Jun_gas'
                  ]

class pledgeForm(ModelForm):
    class Meta:
        model = energyPledge
        fields = [
            'goal', 'end_date'
        ]
        widgets = {
            'end_date': TextInput(attrs={'required': 'true'})
        }