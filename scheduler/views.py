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
            address=data.get('address', '')
            email=data.get('email', '')
            service=data.get('service')
            price=data.get('price')
            date=data.get('date')
            time=data.get('time')
            payment_method=data.get('payment_method', '')
            status_appointment=data.get('status', 'pending')

            if not all([client_name, phone_number, address, email, service, price, date, time, payment_method, status_appointment]):
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
                address=address,
                email=email,
                service=service,
                price=price,
                date=date,
                time=time,
                payment_method=payment_method,
                status=status_appointment,
            )

            return Response({
                "id": appointment.id,
                "client_name": appointment.client_name,
                "phone_number": appointment.phone_number,
                "address": appointment.address,
                "email": appointment.email,
                "service": appointment.service,
                "price": str(appointment.price),
                "date": appointment.date,
                "time": appointment.time,
                "payment_method": appointment.payment_method,
                "status": appointment.status,
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
            "address": appointment.address,
            "email": appointment.email,
            "service": appointment.service,
            "price": str(appointment.price),
            "date": appointment.date,
            "time": appointment.time,
            "payment_method": appointment.payment_method,
            "status": appointment.status,
            "created_at": appointment.created_at,
            "updated_at": appointment.updated_at
        } for appointment in appointments]
        
        return Response(data, status=status.HTTP_200_OK)
    
class UpdateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, appointment_id):
        user = request.user
        data = request.data

        try:
            appointment = Appointment.objects.get(id=appointment_id, user_id=user)
            
            appointment.client_name = data.get('client_name', appointment.client_name)
            appointment.phone_number = data.get('phone_number', appointment.phone_number)
            appointment.address = data.get('address', appointment.address)
            appointment.email = data.get('email', appointment.email)
            appointment.service = data.get('service', appointment.service)
            appointment.price = data.get('price', appointment.price)
            appointment.date = data.get('date', appointment.date)
            appointment.time = data.get('time', appointment.time)
            appointment.payment_method = data.get('payment_method', appointment.payment_method)
            appointment.status = data.get('status', appointment.status)

            conflict = Appointment.objects.filter(
                user_id=user, 
                date=appointment.date, 
                time=appointment.time
            ).exclude(id=appointment.id).exists()

            if conflict:
                return Response({"error": "Conflito de agendamento."}, status=status.HTTP_400_BAD_REQUEST)

            appointment.save()

            return Response({
                "id": appointment.id,
                "client_name": appointment.client_name,
                "phone_number": appointment.phone_number,
                "address": appointment.address,
                "email": appointment.email,
                "service": appointment.service,
                "price": str(appointment.price),
                "date": appointment.date,
                "time": appointment.time,
                "payment_method": appointment.payment_method,
                "status": appointment.status,
                "created_at": appointment.created_at,
                "updated_at": appointment.updated_at
            }, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({"error": "Agendamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
