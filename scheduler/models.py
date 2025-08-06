from django.db import models

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('canceled', 'Cancelado'),
    ]

    user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='appointments')
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service} com {self.client_name} em {self.date} às {self.time}"

    class Meta:
        unique_together = ('user_id', 'date', 'time')