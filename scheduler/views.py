from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from scheduler.models import Appointment
from rest_framework import status

class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        try:
            client_name=data.get('client_name')
            phone_number=data.get('phone_number')
            service=data.get('service')
            date=data.get('date')
            time=data.get('time')
            status_appointment=data.get('status', 'pending')
            price=data.get('price')

            if not all([client_name, phone_number, service, date, time, status_appointment, price]):
                return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
            
            conflict = Appointment.objects.filter(
                user_id=user, 
                date=date, 
                time=time
            ).exists()

            if conflict:
                return Response({"error": "Conflito de agendamento."}, status=status.HTTP_400_BAD_REQUEST)

            appointment = Appointment.objects.create(
                user_id=user,
                client_name=client_name,
                phone_number=phone_number,
                service=service,
                date=date,
                time=time,
                status=status_appointment,
                price=price
            )

            return Response({
                "id": appointment.id,
                "client_name": appointment.client_name,
                "phone_number": appointment.phone_number,
                "service": appointment.service,
                "date": appointment.date,
                "time": appointment.time,
                "status": appointment.status,
                "price": str(appointment.price),
                "created_at": appointment.created_at,
                "updated_at": appointment.updated_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AllAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user_id=user).order_by('-created_at')
        data = [{
            "id": appointment.id,
            "client_name": appointment.client_name,
            "phone_number": appointment.phone_number,
            "service": appointment.service,
            "date": appointment.date,
            "time": appointment.time,
            "status": appointment.status,
            "price": str(appointment.price),
            "created_at": appointment.created_at,
            "updated_at": appointment.updated_at
        } for appointment in appointments]
        
        return Response(data, status=status.HTTP_200_OK)