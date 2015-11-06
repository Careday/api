from django import forms
# from django.contrib.auth.models import User

from .models import Child, DailyReport, Diapering
# Create the form class.


class ChildForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = ('first_name', 'gender', 'birthday',
                  'parent_name', 'parent_email', 'parent_phone')


class DailyReportForm(forms.ModelForm):

    class Meta:
        model = DailyReport
        fields = ('date', 'child', 'arrival_time', 'departure_time',
                  'mood_am', 'mood_pm')


class DiaperForm(forms.ModelForm):

    class Meta:
        model = Diapering
        fields = ('time_diaper', 'num_one', 'num_two', 'comments')
