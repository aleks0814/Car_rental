"""rental_company URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from viewer.views import CarCategoryCreateView, CarCategoryReadView, ClientLoginView, ClientTaskList, ClientTaskDetail, \
    ClientTaskCreate, ClientTaskUpdate, ClientTaskDelete, ClientRegisterPage, UserUpdateView
from viewer.views import CarBrandCreateView, CarBrandReadView
from viewer.views import CarCreateView, CarReadView
from viewer.views import RentalCreateView, RentalReadView
from viewer.views import CarModelCreateView, CarModelReadView
from viewer.views import BookingList, BookingView
from viewer.views import ClientReadView
from viewer.views import ClientCreateView
from viewer.views import ClientSelectUpdateView
from viewer.views import ClientDeleteView
from viewer.views import CarDeleteView
from viewer.views import CarUpdateView
from viewer.views import RentalChosenView
from viewer.views import RentalSelectView
from django.views.generic import TemplateView, RedirectView
import rental_company
from viewer.views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = rental_company

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('carbrand', CarBrandReadView.as_view(), name='carbrand'),
    path('create/carbrand', CarBrandCreateView.as_view()),
    path('carcategory', CarCategoryReadView.as_view(), name='carcategory'),
    path('create/carcategory', CarCategoryCreateView.as_view()),
    path('carmodel', CarModelReadView.as_view(), name='carmodel'),
    path('create/carmodel', CarModelCreateView.as_view()),
    path('rental', RentalReadView.as_view(), name='rental'),
    path('create/rental', RentalCreateView.as_view()),
    path('employee/selectrental/<rental>', RentalChosenView.as_view(), name='selectrental'),
    path('employee/selectrental', RentalSelectView.as_view(), name='rentalchoices'),
    path('car', CarReadView.as_view(), name='car'),
    path('booking_list/', BookingList.as_view(), name='booking_list'),
    path('book/', BookingView.as_view(), name='booking_view'),
    path('create/car', CarCreateView.as_view(), name='create_car'),
    path('update/car/<pk>', CarUpdateView.as_view(), name='update_car'),
    path('delete/car/<pk>', CarDeleteView.as_view(), name='delete_car'),
    path('read/client', ClientReadView.as_view(), name='client'),
    path('create/client', ClientCreateView.as_view(), name='data_list'),
    path('select/update/client', ClientSelectUpdateView.as_view()),
    path('delete/client/<pk>', ClientDeleteView.as_view(), name='delete'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('tasks', TaskList.as_view(), name='tasks'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('task/<pk>/', TaskDetail.as_view(), name='tasks'),
    path('task-create', TaskCreate.as_view(), name='task-create'),
    path('task-update/<pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<pk>/', TaskDelete.as_view(), name='task-delete'),
    path('redirect1', RedirectView.as_view(url='http://127.0.0.1:8000/create/car'), name='createcar'),
    path('redirect2', RedirectView.as_view(url='http://127.0.0.1:8000/create/carbrand'), name='carbrand'),
    path('redirect3', RedirectView.as_view(url='http://127.0.0.1:8000/employee/selectrental'), name='selectrental'),
    path('redirect4', RedirectView.as_view(url='http://127.0.0.1:8000/booking_list/'), name='bookinglist'),
    path('redirect5', RedirectView.as_view(url='http://127.0.0.1:8000/book/'), name='bookacar'),
    path('loginclient/', ClientLoginView.as_view(), name='client_login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout_client'),
    path('clientprofil/', ClientTaskList.as_view(), name='profil'),
    path('task-client', ClientTaskDetail.as_view(), name='task-client'),
    path('task/create/client', ClientTaskCreate.as_view(), name='task-create-client'),
    path('task/update/client', ClientTaskUpdate.as_view(), name='task-update-client'),
    path('task/delete/client', ClientTaskDelete.as_view(), name='task-delete-client'),
    path('register/', ClientRegisterPage.as_view(), name='register'),
    path('redirect6', RedirectView.as_view(url='http://127.0.0.1:8000/register/'), name='register'),
    path('update/user', UserUpdateView.as_view(), name='update_user')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
