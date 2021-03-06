import os
from django.db import models
from django.utils import timezone
# from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


# Assume 'dailyreport_id' is defined.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Child(models.Model):
    BOY = 'B'
    GIRL = 'G'
    GENDER_CHOICES = (
        (BOY, 'Boy'),
        (GIRL, 'Girl'),
    )
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default=BOY)

    first_name = models.CharField(max_length=20)
    birthday = models.DateField(blank=True, null=True)
    parent_name = models.CharField(max_length=20, blank=True, null=True)
    parent_email = models.EmailField(max_length=254, blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)
    # child_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    image = models.ImageField(upload_to='static/img/', blank=True, null=True)

    class Meta:
            verbose_name = 'Child'
            verbose_name_plural = 'Children'
            ordering = ['first_name']

    def __str__(self):
        return ("{}".format(self.first_name))


class DailyReport(models.Model):
    HAPPY = 'HA'
    FINE = 'FI'
    LITTLE_FUSSY = 'LF'
    VERY_FUSSY = 'VF'
    NOT_WELL = 'NW'
    MOOD_CHOICE = (
        (HAPPY, 'Happy'),
        (FINE, 'Fine'),
        (LITTLE_FUSSY, 'A Little Fussy'),
        (VERY_FUSSY, 'Very Fussy'),
        (NOT_WELL, 'Not Well'),
    )
    date = models.DateField(default=timezone.now)   # default = Year-Mo-Day
    child = models.ForeignKey(Child)   # Assume '_id' will be added to 'child'
    arrival_time = models.TimeField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    mood_am = models.CharField(max_length=2,
                               choices=MOOD_CHOICE,
                               default=HAPPY)
    mood_pm = models.CharField(max_length=2,
                               choices=MOOD_CHOICE,
                               default=HAPPY)

    class Meta:
        verbose_name = 'Daily Report'
        verbose_name_plural = 'Daily Reports'
        ordering = ['-date']

    def __str__(self):
        return ("{} : {}".format(self.child.first_name, self.date))


class Diapering(models.Model):
    # assumed diapering_id
    dailyreport = models.ForeignKey(DailyReport)
    time_diaper = models.TimeField()
    num_one = models.BooleanField()  # default is None when empty
    num_two = models.BooleanField()
    comments = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
                verbose_name = 'Diapering'
                verbose_name_plural = 'Diapering'
                ordering = ['dailyreport', 'time_diaper']

class Sleeping(models.Model):
    # assumed sleeping_id
    dailyreport = models.ForeignKey(DailyReport)
    time_slp_start = models.TimeField(blank=True, null=True)
    time_slp_end = models.TimeField(blank=True, null=True)

    class Meta:
                verbose_name = 'Sleeping'
                verbose_name_plural = 'Sleeping'
                ordering = ['dailyreport', 'time_slp_start']

class Eating(models.Model):
    # assumed eating_id
    BOTTLE = 'BOTTLE'
    NURSED = 'NURSED'
    FOOD = 'FOOD'
    NONE = 'NONE'
    ONE_QUARTER = '1_QUARTER'
    ONE_HALF = '1_HALF'
    THREE_QUARTER = '3_QUARTER'
    ALL = 'ALL'
    FOOD_CHOICE = (
        (BOTTLE, 'Bottle'),
        (NURSED, 'Nursed'),
        (FOOD, 'Food'),
    )
    LEFTOVER = (
        (NONE, 'None leftover'),
        (ONE_QUARTER, '1/4 leftover'),
        (ONE_HALF, '1/2 leftover'),
        (THREE_QUARTER, '3/4 leftover'),
        (ALL, 'All leftover'),
    )
    dailyreport = models.ForeignKey(DailyReport)
    time_eat = models.TimeField(blank=True, null=True)
    food = models.CharField(max_length=6,
                            choices=FOOD_CHOICE,
                            blank=True,
                            null=True)
    leftover = models.CharField(max_length=9,
                                choices=LEFTOVER,
                                blank=True,
                                null=True)
    class Meta:
                verbose_name = 'Eating'
                verbose_name_plural = 'Eating'
                ordering = ['dailyreport', 'time_eat']