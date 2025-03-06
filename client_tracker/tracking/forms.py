from django import forms

from .models import Customer, Job, Services, User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ["created_by"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Capture the request object
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.created_by = self.request.user  # Set created_by to the authenticated user
        if commit:
            instance.save()
        return instance

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

        labels = {
            "username": "Kullanıcı Adı:",
            "first_name": "Ad:",
            "last_name": "Soyad:",
            "email": "E-posta:",
            "password1": "Şifre:",
            "password2": "Şifre (Tekrar):",
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kullanıcı Adı"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ad"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Soyad"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-posta"}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # Password alanlarına Bootstrap form-control sınıfı ekleme
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Şifre"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Şifre Tekrar"})
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ["name", "price", "is_active"]

        labels = {
            "name": "Servis Adı:",
            "price": "Ücret:",
            "is_active": "Aktif mi? :",
           
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kullanıcı Adı"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ücret"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }

from django_select2.forms import Select2Widget
from django import forms
from .models import Job
from django_select2.forms import Select2Widget

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["employee", "customer", "service", "price", "vat", "total_price", "info", "appointment_date","appointment_time"]
        widgets = {
            "employee": Select2Widget(attrs={"class": "form-control"}),  # Select2
            "customer": Select2Widget(attrs={"class": "form-control"}),  # Select2
            "service": Select2Widget(attrs={"class": "form-control"}),   # Select2
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Fiyat girin"}),
            "vat": forms.NumberInput(attrs={"class": "form-control", "placeholder": "KDV oranı (%)"}),
            "appointment_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": "Appointment Date", "type": "date"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"class": "form-control", "placeholder": "Appointment Date", "type": "time"}
            ),
            "info": forms.Textarea(attrs={"class": "form-control", "placeholder": "Bilgi girin"}),
            "total_price": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),  # Sadece okunabilir
        }


    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields["employee"].queryset = User.objects.all()  # Tüm kullanıcıları listele
        self.fields["customer"].queryset = Customer.objects.all()  # Tüm müşterileri listele
        self.fields["service"].queryset = Services.objects.filter(is_active=True)  # Tüm hizmetleri listele

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        vat = cleaned_data.get("vat")

        if price is not None and vat is not None:
            total_price = price + (price * vat / 100)  # KDV dahil toplam fiyat
            cleaned_data["total_price"] = total_price  # Form verisine ekle
        else:
            cleaned_data["total_price"] = None  # Boş bırak

        return cleaned_data
