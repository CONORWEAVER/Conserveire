from django.db import models
from django.db.models import ForeignKey
from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Create your models here.

COUNTY_CHOICES = [
    ('Cork', 'Cork'),
    ('Dublin', 'Dublin'),
    ('Kerry', 'Kerry'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    county = models.CharField(max_length=20, choices=COUNTY_CHOICES)

    def __str__(self):
        return self.user.username


# create and save user profile object
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])



post_save.connect(create_profile, sender=User)


# monthly usage model, unique for logged in user, blank=True for month
# fields to facilitate partial form submission and conditional field rendering
class Usage(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    Jan = models.IntegerField(default=0, blank=True)
    Feb = models.IntegerField(default=0, blank=True)
    Mar = models.IntegerField(default=0, blank=True)
    Apr = models.IntegerField(default=0, blank=True)
    May = models.IntegerField(default=0, blank=True)
    Jun = models.IntegerField(default=0, blank=True)
    Jul = models.IntegerField(default=0, blank=True)
    Aug = models.IntegerField(default=0, blank=True)
    Sep = models.IntegerField(default=0, blank=True)
    Oct = models.IntegerField(default=0, blank=True)
    Nov = models.IntegerField(default=0, blank=True)
    Dec = models.IntegerField(default=0, blank=True)
    electricity = models.IntegerField(default=0, blank=True)
    oil = models.IntegerField(default=0, blank=True)
    gas = models.IntegerField(default=0, blank=True)
    oil_frequency = models.IntegerField(default=0, blank=True)
    county = models.CharField(max_length=25, choices=COUNTY_CHOICES, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    standing_charge = models.IntegerField(default=0, blank=True)
    difference = models.IntegerField(default=0, blank=True)
    rate = models.FloatField(default=0, blank=True)
    reduction_percentage = models.IntegerField(default=0, blank=True)
    submitted = models.DateField(auto_now_add='TRUE'),
