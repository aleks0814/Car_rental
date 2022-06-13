from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import forms
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View, FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from viewer.forms.car_brand import CarBrandForm
from viewer.forms.car_category import CarCategoryForm
from viewer.forms.car_model import CarModelForm
from viewer.forms.registration import RegistrationForm
from viewer.forms.rental import RentalForm
from viewer.forms.rental import RentalSelectForm
from viewer.forms.car import CarForm
from viewer.forms.functions import Availability
from viewer.forms.client import ClientForm
from viewer.forms.client import ClientSelect
from viewer.models import Client
from viewer.models import ClientTask
from viewer.models import CarBrand
from viewer.models import CarCategory
from viewer.models import CarModel
from viewer.models import Rental
from viewer.models import Car
from viewer.models import Booking
from viewer.models import Task
from viewer.booking_functions.availability import check_availability
from bs4 import BeautifulSoup
import requests
import re
import arrow
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from fpdf import FPDF

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CarBrandReadView(PermissionRequiredMixin, TemplateView):
    permission_required = 'viewer.view_carbrand'
    template_name = 'car_brand.html'
    extra_context = {'data': CarBrand.objects.all()}


class CarBrandCreateView(PermissionRequiredMixin, FormView):
    permission_required = 'viewer.add_carbrand'
    template_name = 'form.html'
    form_class = CarBrandForm
    success_url = reverse_lazy('carbrand')

    def form_valid(self, form):
        result = super().form_valid(form)
        my_data = form.cleaned_data
        CarBrand.objects.create(
            name=my_data['name']
        )

        return result


class CarCategoryReadView(PermissionRequiredMixin,TemplateView):
    permission_required = 'viewer.view_carcategory'
    template_name = 'car_category.html'
    extra_context = {'data': CarCategory.objects.all()}


class CarCategoryCreateView(PermissionRequiredMixin,FormView):
    permission_required = 'viewer.add_carcategory'
    template_name = 'form.html'
    form_class = CarCategoryForm
    success_url = reverse_lazy('carcategory')

    def form_valid(self, form):
        result = super().form_valid(form)
        my_data = form.cleaned_data
        CarCategory.objects.create(
            name=my_data['name']
        )

        return result


class CarModelReadView(TemplateView):
    template_name = 'car_model.html'
    extra_context = {'data': CarModel.objects.all().order_by('car_brand__name')}


class CarModelCreateView(PermissionRequiredMixin,FormView):
    permission_required = 'viewer.add_carmodel'
    template_name = 'form.html'
    form_class = CarModelForm
    success_url = reverse_lazy('carmodel')

    def form_valid(self, form):
        result = super().form_valid(form)
        my_data = form.cleaned_data
        CarModel.objects.create(
            car_category=my_data['car_category'],
            car_brand=my_data['car_brand'],
            name=my_data['name'],
            capacity=my_data['capacity'],
            picture=my_data['picture']
        )

        return result


class RentalReadView(PermissionRequiredMixin, TemplateView):
    permission_required = 'viewer.view_rental'
    template_name = 'rental.html'
    extra_context = {'data': Rental.objects.all(), }


class RentalCreateView(PermissionRequiredMixin,FormView):
    permission_required = 'viewer.add_rental'
    template_name = 'form.html'
    form_class = RentalForm
    success_url = reverse_lazy('rental')

    def form_valid(self, form):
        result = super().form_valid(form)
        my_data = form.cleaned_data
        Rental.objects.create(
            name=my_data['name'],
            address=my_data['address'],
            number_of_cars=my_data['number_of_cars']
        )

        return result


class RentalChosenView(PermissionRequiredMixin,LoginRequiredMixin, View):
    permission_required = 'viewer.view_rental'
    def get(self, req, rental):
        data = Car.objects.filter(rental__name=rental).order_by('price_per_day')
        access = str(rental).lower()
        if access == 'paryż':
            access = 'paryz'
        if not self.request.user.has_perm(f'viewer.{access}_view_car'):
            raise PermissionDenied
        return render(req, 'car.html', context={'data': data})


class RentalSelectView(PermissionRequiredMixin,LoginRequiredMixin, FormView):
    permission_required = 'viewer.view_rental'
    template_name = 'form.html'
    form_class = RentalSelectForm

    def form_valid(self, form):
        return redirect('selectrental', rental=form.cleaned_data['rental'].name)


class CarReadView(PermissionRequiredMixin,TemplateView):
    permission_required = 'viewer.view_car'
    template_name = 'car.html'
    extra_context = {'data': Car.objects.all().order_by('-rental')}


class CarCreateView(PermissionRequiredMixin,LoginRequiredMixin, FormView):
    permission_required = 'viewer.add_car'
    template_name = 'form.html'
    form_class = CarForm
    success_url = reverse_lazy('rentalchoices')
    model = Car

    def form_valid(self, form):
        result = super().form_valid(form)
        my_data = form.cleaned_data
        Car.objects.create(
            car_model=my_data['car_model'],
            rental=my_data['rental'],
            transmission=my_data['transmission'],
            air_conditioning=my_data['air_conditioning'],
            price_per_day=my_data['price_per_day'],
            avability=my_data['avability']
        )
        Rental.objects.filter(name=my_data['rental']).update(number_of_cars=F('number_of_cars') + 1)

        return result


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = 'update_form.html'
    fields = ['price_per_day', 'avability']

    def get_login_url(self):
        return self

    def get_object(self, *args, **kwargs):
        obj = super(CarUpdateView, self).get_object(*args, **kwargs)
        access = str(obj.rental).lower()
        if access == 'paryż':
            access = 'paryz'
        if not self.request.user.has_perm(f'viewer.{access}_view_car'):
            raise PermissionDenied
        return obj

    def get_success_url(self, *args, **kwargs):
        view_name = 'selectrental'
        return reverse_lazy(view_name, kwargs={'rental': self.object.rental})


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'form_delete.html'

    def get_object(self, *args, **kwargs):
        obj = super(CarDeleteView, self).get_object(*args, **kwargs)
        access = str(obj.rental).lower()
        if access == 'paryż':
            access = 'paryz'
        if not self.request.user.has_perm(f'viewer.{access}_view_car'):
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        Rental.objects.filter(pk=self.object.rental.pk).update(number_of_cars=F('number_of_cars') - 1)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self, *args, **kwargs):
        view_name = 'selectrental'
        return reverse_lazy(view_name, kwargs={'rental': self.object.rental})


class ClientReadView(View):
    def get(self, request):
        Client.objects.all()
        return render(request, "client_read.html", context={'data': Client.objects.all()})


# client creates his own profile
class ClientCreateView(FormView):
    template_name = 'client_create.html'
    success_url = reverse_lazy('client')
    form_class = ClientForm

    def form_valid(self, form):
        result = super().form_valid(form)
        data = form.cleaned_data
        Client.objects.create(
            name=data['name'],
            surname=data['surname'],
            login=data['login'],
            email=data['email'],
            password=data['password'],
            document_id=data['document_id']
        )
        return redirect('data_list')


# client can update his own data in profile
class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'viewer/client_update_form.html'
    # form_class = RegistrationForm
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy("profil")

    def get_object(self, **kwargs):
        return self.request.user

class ClientSelectUpdateView(FormView):
    form_class = ClientSelect
    template_name = 'form.html'

    def form_valid(self, form):
        return redirect('client_update', pk=form.cleaned_data['client'].id)


# root/admin can delete a client
class ClientDeleteView(DeleteView):
    template_name = 'client_delete.html'
    model = Client
    success_url = reverse_lazy("client")


class BookingList(PermissionRequiredMixin, ListView):
    permission_required = 'viewer.view_task'
    model = Booking
    template_name = 'booking_list.html'

    #####################Funkcja##########################


def send_pdf_document(booking_id, name, car_name, date_of_rental, date_of_return, total_cost,rental):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", size=25)
    pdf.cell(200, 10, txt="Car Booking Confirmation",
             ln=1, align='C')
    pdf.line(x1=50, y1=20, x2=170, y2=20)
    pdf.set_font("Arial", size=15)

    pdf.cell(200, 10, txt=f"Booking number:{booking_id}",
             ln=2, align='C')
    pdf.ln(50)
    pdf.cell(200, 10, txt=f"Hi {name}, thanks for your booking!",
             ln=2, align='C')
    pdf.cell(200, 10, txt=f"You've booked {car_name} from {date_of_rental} to {date_of_return}.",
             ln=2, align='C')
    pdf.cell(200, 10, txt=f"Please visit us in our office to pick up your car adress: ",
             ln=2, align='C')
    pdf.cell(200, 10, txt=f" {rental} ",
             ln=2, align='C')
    pdf.set_font("Arial", "U", size=20)
    pdf.ln(50)
    pdf.cell(200, 10, txt="Booking Summary:",
             ln=1, align='C')
    pdf.set_font("Arial", "I", size=15)
    pdf.ln(10)
    pdf.set_fill_color(211, 211, 211)
    pdf.cell(190, 10, txt=f"Total:{total_cost}$    ", border=1, fill=True,
             ln=0, align='R')
    pdf.output("confirmation.pdf")


def send_pdf_by_mail(mail):
    message = Mail(
        from_email='car.rental@interia.pl',
        to_emails=mail,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=f'<strong>Greetings! We\'ve booked a car for You. Feel free to check the attached file for all valuable information.</strong>')

    with open('confirmation.pdf', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('confirmation.pdf'),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attachedFile
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/rome?unitGroup=metric&include=current&key=9KXDRMLE3LP3CR8497HUAQZDD&contentType=json"


class BookingView(LoginRequiredMixin, FormView):
    login_url = 'http://127.0.0.1:8000/loginclient/'
    redirect_field_name = 'booking_view'
    template_name = 'book.html'
    form_class = Availability

    def get_success_url(self):
        return reverse_lazy('client_login_booking')

    def gasoline_price(self, city_name):
        url = f"https://www.expatistan.com/price/gas/{city_name}"
        gasoline_page = requests.get(url, verify=False)
        scraped = BeautifulSoup(gasoline_page.content, "html.parser")
        raw_data = scraped.find("h1")
        result = "".join(
            map(str, [re.sub('\n|</?\w*\s?\w*=?\"?\w*-?\d?\"?>|\s{16}', "", str(i)) for i in raw_data]))
        return result

    def get_weather(self, city_name):
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&include=current&key=9KXDRMLE3LP3CR8497HUAQZDD&contentType=json"
        weather_req = requests.get(url, verify=False)
        weather = weather_req.json()
        city = weather["address"].capitalize()
        temp = weather["days"][0]["temp"]
        conditions = weather["days"][0]["conditions"]
        return [city, temp, conditions]

    def form_valid(self, form):
        result = super().form_valid(form)
        return result

    def post(self, request, *args, **kwargs):
        if 'search_cars' in request.POST:
            return self.search_cars(request)
        elif 'book_car' in request.POST:
            return self.book_car(request)
        else:
            return HttpResponse('Request not supported.')

    def search_cars(self, request):
        formset = Availability(request.POST)

        CITIES = {
            'Rzym': 'rome',
            'Paryż': 'paris',
            'Londyn': 'london'
        }
        if formset.is_valid():
            data = formset.cleaned_data
            weather_data = self.get_weather(CITIES[str(data['rental'])])
            gasoline_price = self.gasoline_price(CITIES[str(data['rental'])])
            return render(request, 'book.html', {
                'gasoline_price': gasoline_price,
                'form': formset,
                'conditions': weather_data[2],
                'temp': weather_data[1],
                'city': weather_data[0],
                'text': self.get_available_car_list(data)[0],
                'rental_time': (arrow.get(data['date_of_return']) - arrow.get(data['date_of_rental'])).days,
                'available_cars': self.get_available_car_list(data)[1:],
            })
        else:
            return HttpResponse('Oooops. Something went wrong. Try again later.')

    def get_available_car_list(self, data):

        if data['air_conditioning']:
            ac = data['air_conditioning']
        else:
            ac = None


        car_list = Car.objects.filter(rental=data['rental'],
                                      car_model__car_category__name__contains=data['category'],
                                      transmission=data['transmission'],
                                      air_conditioning=ac)

        available_cars_filter = []

        for car in car_list:
            if check_availability(car, data['date_of_rental'], data['date_of_return']):
                available_cars_filter.append(car)

        other_cars = Car.objects.filter(rental=data['rental'])

        all_available_cars = []
        for car in other_cars:
            if check_availability(car, data['date_of_rental'], data['date_of_return']):
                all_available_cars.append(car)

        text_1 = " Sorry, at the time We don't have any cars that match your criteria, " \
                 "Here is a list of other cars available by this date, in this city"
        text = "Here's your cars"

        if available_cars_filter:
            available_cars_filter.insert(0, text)
            available_cars = available_cars_filter
        else:
            all_available_cars.insert(0, text_1)
            available_cars = all_available_cars

        return available_cars

    def book_car(self, request):
        formset = Availability(request.POST)
        if formset.is_valid():
            data = formset.cleaned_data
        date_of_rental = data['date_of_rental']
        date_of_return = data['date_of_return']
        date_of_rental_for_count = arrow.get(data['date_of_rental'])
        date_of_return_for_count = arrow.get(data['date_of_return'])
        number_of_days = date_of_return_for_count - date_of_rental_for_count
        number_of_days = number_of_days.days
        request_data = request.POST
        car = Car.objects.get(pk=request_data['book_car'])
        total_cost = number_of_days * car.price_per_day
        booking = Booking.objects.create(
            user=self.request.user,
            car=car,
            date_of_rental=date_of_rental,
            date_of_return=date_of_return,
            approved=True,
            days_to_return=1,
            number_of_days=number_of_days,
            penalties=False,
            amount_of_penalties=1,
            insurance=False,
            total_cost=total_cost,
        )
        booking.save()

        send_pdf_document(
            booking_id=booking.id,
            name=self.request.user,
            car_name=car,
            date_of_rental=date_of_rental,
            date_of_return=date_of_return,
            total_cost=total_cost,
            rental=car.rental.address,

        )

        send_pdf_by_mail(self.request.user.email)

        return render(request, 'final_booking.html',{
            'user': self.request.user,
            'booking_id': booking.id,
            'car': car,

        })



class TemplateLoginView(LoginView):
    template_name = 'viewer/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('template')


url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/rome?unitGroup=metric&include=current&key=9KXDRMLE3LP3CR8497HUAQZDD&contentType=json"


class TemplateView(TemplateView):
    template_name = 'home'
    # context_object_name = 'template'
    context = 'template'

    def get_context_data(self, **kwargs):
        testowa_zmienna = 10
        weather_req = requests.get(url, verify=False)
        weather = weather_req.json()
        city = weather["address"].capitalize()
        temp = weather["days"][0]["temp"]
        conditions = weather["days"][0]["conditions"]
        context = super().get_context_data(**kwargs)
        context['city'] = city
        context['temp'] = temp
        context['conditions'] = conditions
        context['testowa_zmienna'] = testowa_zmienna
        print(context)
        return context


class CustomLoginView(LoginView):
    """Part of code related to worker platform"""
    template_name = 'viewer/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/rome?unitGroup=metric&include=current&key=9KXDRMLE3LP3CR8497HUAQZDD&contentType=json"


def get_weather(city_name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&include=current&key=9KXDRMLE3LP3CR8497HUAQZDD&contentType=json"
    weather_req = requests.get(url, verify=False)
    weather = weather_req.json()
    city = weather["address"].capitalize()
    temp = weather["days"][0]["temp"]
    conditions = weather["days"][0]["conditions"]
    return [city, temp, conditions]


class TaskList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'viewer.change_task'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        paris_weather = get_weather('paris')
        rome_weather = get_weather('rome')
        london_weather = get_weather('london')
        weather = zip(paris_weather, rome_weather, london_weather)
        context['weather'] = weather
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'viewer/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class ClientLoginView(LoginView):
    """Part of code related to client platform"""
    template_name = 'viewer/client_login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profil')

class ClientRegisterPage(FormView):
    template_name = 'viewer/register.html'
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profil')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(ClientRegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profil')
        return super(ClientRegisterPage, self).get(*args, **kwargs)


class ClientTaskList(LoginRequiredMixin, ListView):
    model = ClientTask
    context_object_name = 'profil'
    template_name = 'viewer/clienttask_list'


class ClientTaskDetail(LoginRequiredMixin, DetailView):
    model = ClientTask
    context_object_name = 'profil'
    template_name = 'viewer/clienttask_list.html'


class ClientTaskCreate(LoginRequiredMixin, CreateView):
    model = ClientTask
    fields = '__all__'
    success_url = reverse_lazy('profil')

    def form_invalid(self, form):
        form.instance.user = self.request.user
        return super(ClientTaskCreate, self).form_valid(form)


class ClientTaskUpdate(LoginRequiredMixin, UpdateView):
    model = ClientTask
    fields = '__all__'
    success_rul = reverse_lazy('profil')


class ClientTaskDelete(LoginRequiredMixin, DeleteView):
    model = ClientTask
    context_object_name = 'profil'
    success_url = reverse_lazy('profil')
