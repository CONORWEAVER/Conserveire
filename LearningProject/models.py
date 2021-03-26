from django.db import models
from django.db.models import ForeignKey
from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

COUNTY_CHOICES = [
    ('cork', 'Cork'),
    ('dublin', 'Dublin'),
    ('kerry', 'Kerry'),
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
    submitted = models.DateField(auto_now_add='TRUE'),
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    jan = models.IntegerField(default=0, blank=True)
    feb = models.IntegerField(default=0, blank=True)
    mar = models.IntegerField(default=0, blank=True)
    apr = models.IntegerField(default=0, blank=True)
    may = models.IntegerField(default=0, blank=True)
    jun = models.IntegerField(default=0, blank=True)
    jul = models.IntegerField(default=0, blank=True)
    aug = models.IntegerField(default=0, blank=True)
    sep = models.IntegerField(default=0, blank=True)
    oct = models.IntegerField(default=0, blank=True)
    nov = models.IntegerField(default=0, blank=True)
    dec = models.IntegerField(default=0, blank=True)
