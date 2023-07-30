import calendar, datetime
from .models import Day


def create_calendar(reference_date):
    if not Day.objects.filter(date=reference_date).exists():
        number_of_days = calendar.monthrange(reference_date.year, reference_date.month)[1]
        for day in range(1, number_of_days + 1):
            day_instance = Day(date=datetime.date(reference_date.year, reference_date.month, day))
            day_instance.save()
    days = Day.objects.filter(date__month=reference_date.month)
    dummy_days = []
    weekday_number = datetime.date(reference_date.year, reference_date.month, 1).weekday()
    if weekday_number < 6:
        for i in range(weekday_number + 1):
            dummy_days.append('dummy_day')
    return days, dummy_days

# def create_appointment_instance(request, selected_date_string):
#     if request.user.is_authenticated:
#         selected_date = datetime.strptime(selected_date_string, '%Y_%m_%d').date()
#         appointment = Day.objects.get(date=selected_date)
#         if not appointment.busy:
#             appointment.busy = True
#             appointment.email = request.user.email
#             appointment.client = request.user
#             appointment.save()
#     else
