from django.db import models
from django.conf import settings
class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Kullanıcıyı tanımlamak için e-posta kullanılıyor.
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
from django.contrib.auth import get_user_model
class Customer(models.Model):
    code = models.CharField(max_length=10, unique=True)
    owner_name = models.CharField(max_length=255)
    owner_surname = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Make sure to get the actual User instance and assign it to created_by
        if not self.created_by and 'user' in kwargs:
            self.created_by = kwargs.pop('user')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand_name} - {self.owner_name} {self.owner_surname}"
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Services(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        # Eğer created_by belirtilmemişse otomatik olarak atanmasını engelle
        if not self.created_by_id and "user" in kwargs:
            self.created_by = kwargs.pop("user")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name}"

class Job(models.Model):
    employee = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='employee_jobs'  # employee için ters ilişki adını değiştiriyoruz
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="jobs")
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    vat = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    info = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_job'  # created_by için ters ilişki
    )
    
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('in_progress', 'İşlemde'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def save(self, *args, **kwargs):
        # Eğer created_by değeri atanmamışsa, oturumdaki kullanıcıyı atayın
        if not self.created_by:
            self.created_by = settings.AUTH_USER_MODEL  # Oturumdaki kullanıcıyı atıyoruz
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.brand_name} - {self.service.name} ({self.employee.first_name})"