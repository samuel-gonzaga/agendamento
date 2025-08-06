

from django.urls import path

from .views import CreateAppointmentView, AllAppointmentsView


urlpatterns = [
    path('create/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('appointments/', AllAppointmentsView.as_view(), name='list_appointments'),
]