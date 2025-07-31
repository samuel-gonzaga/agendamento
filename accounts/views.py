from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Todos os campos são obrigatórios.'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email já cadastrado.'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'Usuário criado com sucesso.', 'id': user.id}, status=201)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })
