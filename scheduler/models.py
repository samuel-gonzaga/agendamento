from django.db import models

class Scheduler(models.Model):
    user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='schedulers')
    client_name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Scheduler'
        verbose_name_plural = 'Schedulers'
        ordering = ['-created_at']