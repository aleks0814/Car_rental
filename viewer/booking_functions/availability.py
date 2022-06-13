import datetime
from viewer.models import Car, Booking


def check_availability(car, date_of_rental, date_of_return):
    avail_list = []
    booking_list = Booking.objects.filter(car=car)
    for booking in booking_list:
        if booking.date_of_rental > date_of_return or booking.date_of_return < date_of_rental:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)