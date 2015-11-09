from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import Child, DailyReport, Diapering, Sleeping, Eating
from .forms import ChildForm, DailyReportForm, DiaperingForm, SleepingForm, EatingForm
from django.contrib.auth.decorators import login_required
# Create your views here.


# Create your views here.
def index(request):
    '''
    returns current time in html
    '''
    now = datetime.now()
    html = "<html><body>Welcome to CareDay! <br> The current time is: {} local server time.</body></html>".format(
        now)
    return HttpResponse(html)


class ChildActionMixin(object):
    fields = ('first_name', 'gender', 'birthday',
              'parent_name', 'parent_email', 'parent_phone')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ChildActionMixin, self).form_valid(form)


class ChildListView(ListView):

    model = Child
    template_name = 'careapp/childs_list.html'


class ChildPickerView(ListView):   # test of children list

    model = Child
    template_name = 'careapp/childs_picker.html'

    def url_1(request):
        unit = DailyReport.objects.get(pk=1)
        unit.date = request.POST['date']
        unit.name = request.POST['name']
        unit.save()
        return HttpResponse('ok')


class ChildCreateView(ChildActionMixin, CreateView):

    model = Child
    # fields = ('first_name', 'gender', 'birthday',
    #           'parent_name', 'parent_email', 'parent_phone')
    #
    template_name = 'careapp/edit_child.html'
    success_msg = "Child created!"

    def get_success_url(self):
        return reverse('childs-list')


class ChildUpdateView(ChildActionMixin, UpdateView):
    # form_class = ChildForm
    model = Child
    # fields = ('first_name', 'gender', 'birthday',
    #           'parent_name', 'parent_email', 'parent_phone')
    template_name_suffix = '_update_form'
    success_msg = "Child updated!"

    def get(self, request, **kwargs):
        self.object = Child.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Child.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('childs-list')


class ChildDetailView(DetailView):
    model = Child


# @login_required
def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.save()
            messages.add_message(request, messages.SUCCESS, 'Child added.')
            return redirect('children-list')
        else:
            messages.add_message(request, messages.ERROR, 'Form data invalid.')

    else:
        form = ChildForm()
    return render(request, 'careapp/edit_child.html',
                  {'form': form})


class DailyReportCreateView(CreateView):

    model = DailyReport
    template_name = 'careapp/daily_report.html'
    fields = ('date', 'child', 'arrival_time',
              'departure_time', 'mood_am', 'mood_pm')


# @login_required
    def daily_report(request):
        '''
        Opens the Daily sign-in form.
        '''
        if request.method == 'POST':
            form = DailyReportForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('daily-report')
        else:
            form = DailyReportCreateView()
        return render(request, 'daily_report.html',
                      {'form': form})

    def get_success_url(self):
        return reverse('daily-report')


# @login_required
# def daily_ending(request):
#     '''
#     opens the end-of-day part of the Daily sign-in form.
#     '''
#     if request.method == 'POST':
#         form = DailyEndingForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('daily-report-ending')
#     else:
#         form = DailyEndingCreateView()
#     return render(request, 'daily_report_ending.html',
#                   {'form': form})

""" DIAPERING TABLES """


class DiaperingMixin(object):
    fields = ('dailyreport', 'time_diaper', 'num_one',
              'num_two', 'comments')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(DiaperingMixin, self).form_valid(form)


class DiaperingCreateView(DiaperingMixin, CreateView):

    model = Diapering
#    template_name = 'careapp/edit_child.html'
    success_msg = "Diapering completed"

    # def get_success_url(self):
    #     return reverse('childs-list')

    def diapering(request):
        '''
        Opens the Diapering activity panel.
        '''
        if request.method == 'POST':
            form = DiaperingForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('diapering')
        else:
            form = DiaperingCreateView()
        return render(request, 'diapering_form.html',
                      {'form': form})

    def get_success_url(self):
        return reverse('diapering')


class DiaperingUpdateView(DiaperingMixin, UpdateView):
    model = Diapering
    success_msg = "Diapering completed"


class DiaperingDetailView(DiaperingMixin, DetailView):
    model = Diapering

""" SLEEPING TABLES """


class SleepingMixin(object):
    fields = ('dailyreport', 'time_slp_start', 'time_slp_end')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(SleepingMixin, self).form_valid(form)


class SleepingCreateView(SleepingMixin, CreateView):

    model = Sleeping
    success_msg = "Sleeping recorded"

    def sleeping(request):
        '''
        Opens the Sleeping activity panel.
        '''
        if request.method == 'POST':
            form = SleepingForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('sleeping')
        else:
            form = SleepingCreateView()
        return render(request, 'sleeping_form.html',
                      {'form': form})

    def get_success_url(self):
        return reverse('sleeping')


class SleepingUpdateView(SleepingMixin, UpdateView):
    model = Sleeping
    success_msg = "Sleeping recorded"


class SleepingDetailView(SleepingMixin, DetailView):
    model = Sleeping


""" EATING TABLES """


class EatingMixin(object):
    fields = ('dailyreport', 'time_eat', 'food', 'leftover')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(EatingMixin, self).form_valid(form)


class EatingCreateView(EatingMixin, CreateView):

    model = Eating
    success_msg = "Food Intake recorded"

    def sleeping(request):
        '''
        Opens the Eating activity panel.
        '''
        if request.method == 'POST':
            form = EatingForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('eating')
        else:
            form = EatingCreateView()
        return render(request, 'eating_form.html',
                      {'form': form})

    def get_success_url(self):
        return reverse('eating')


class EatingUpdateView(EatingMixin, UpdateView):
    model = Eating
    success_msg = "Food Intake recorded"


class EatingDetailView(EatingMixin, DetailView):
    model = Eating
