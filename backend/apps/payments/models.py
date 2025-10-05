from django.db import models

class Payment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    method = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"