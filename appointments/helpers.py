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

