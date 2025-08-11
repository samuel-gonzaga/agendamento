

from django.urls import path

from .views import CreateAppointmentView, AllAppointmentsView, UpdateAppointmentView, DeleteAppointmentView


urlpatterns = [
    path('create/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('appointments/', AllAppointmentsView.as_view(), name='list_appointments'),
    path('update/<int:appointment_id>/', UpdateAppointmentView.as_view(), name='update_appointment'),
    path('delete/<int:appointment_id>/', DeleteAppointmentView.as_view(), name='delete_appointment'),
]