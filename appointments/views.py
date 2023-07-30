from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from .helpers import create_calendar
from .models import Day, User
from .forms import AppointmentRegistrationForm, LoginAndAppointmentRegistrationForm
import urllib.parse
import json


def create_appointment(request):
    if request.user.is_authenticated:
        return redirect(reverse('galleries:display_user_galleries'))
    if request.method == 'POST':
        form = AppointmentRegistrationForm(request.POST)
        if form.is_valid():
            selected_date_string = request.POST.get('selected_date')
            if selected_date_string:
                email = request.POST.get('email')
                if (not request.user.is_authenticated) and User.objects.filter(email=email).exists():
                    hidden_form_data = dict(request.POST)
                    if 'csrfmiddlewaretoken' in hidden_form_data: del hidden_form_data['csrfmiddlewaretoken']
                    json_encoded_data = urllib.parse.quote(json.dumps(hidden_form_data))
                    return redirect(reverse('appointments:login_and_create_appointment') + f'?data={json_encoded_data}')

                selected_date = datetime.strptime(selected_date_string, '%Y_%m_%d').date()
                appointment = Day.objects.get(date=selected_date)
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                message = request.POST.get('message')
                phone = request.POST.get('phone')
                if not appointment.busy:
                    appointment.busy = True
                    appointment.client = None
                    appointment.email = email
                    appointment.message = message
                    appointment.phone = phone
                    appointment.first_name = first_name
                    appointment.last_name = last_name
                    appointment.save()
                    return render(request,
                                  'appointments/login_and_create_appointment_success.html',
                                  {})
                else:
                    form.add_error('', 'The date you\'ve selected is already booked. Please select another date')
            else:
                form.add_error('', 'Please select the date for your appointment')
    else:
        form = AppointmentRegistrationForm()

    today = date.today()
    this_month_name = today.strftime('%B')
    this_month_days, this_month_dummy_days = create_calendar(today)
    next_month_date = today + relativedelta(months=1)
    next_month_name = next_month_date.strftime('%B')
    next_month_days, next_month_dummy_days = create_calendar(next_month_date)
    return render(request,
                  'appointments/create_appointment.html',
                  {'form': form,
                   'this_month_name': this_month_name,
                   'this_month_days': this_month_days,
                   'this_month_dummy_days': this_month_dummy_days,
                   'next_month_name': next_month_name,
                   'next_month_days': next_month_days,
                   'next_month_dummy_days': next_month_dummy_days})


def login_and_create_appointment(request):
    if request.method == 'POST':
        form = LoginAndAppointmentRegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            selected_date_string = request.POST.get('selected_date')
            selected_date = datetime.strptime(selected_date_string, '%Y_%m_%d').date()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            appointment = Day.objects.get(date=selected_date)

            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if not appointment.busy:
                    login(request, user)
                    appointment.busy = True
                    appointment.client = request.user
                    appointment.email = user.email
                    appointment.message = message
                    appointment.phone = user.phone
                    appointment.first_name = user.first_name
                    appointment.last_name = user.last_name
                    appointment.save()
                    return render(request,
                                  'appointments/login_and_create_appointment_success.html',
                                  {})
                else:
                    form.add_error('', 'The date you\'ve selected is already booked. Please select another date')
            else:
                form.add_error('password', 'Please enter a correct password')
    else:
        hidden_form_fields = request.GET.get('data')
        if not hidden_form_fields:
            return redirect('galleries:display_homepage')
        decoded = json.loads(urllib.parse.unquote(hidden_form_fields))
        decoded_dictionary = {key: value[0] for key, value in decoded.items()}
        form = LoginAndAppointmentRegistrationForm(initial=decoded_dictionary)
    return render(request,
                  'appointments/login_and_create_appointment.html',
                  {'form': form})
