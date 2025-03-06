import json
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomerForm, EmployeeForm, JobForm, ServiceForm
from .models import Customer, Job, Payment, Services, User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now, timedelta
# Create your views here.
def dashboard(request):
    customers = get_customers() or []  # Eğer None dönerse boş liste ata
    context = {
        'customers': customers,
    }
    return render(request, 'dashboard.html', context)
# customer
def get_customers():
    return Customer.objects.all()
# employee
def get_employee():
    from django.contrib.auth.models import User  # Veya özel modelin varsa get_user_model() kullan
    return User.objects.all()
def get_services():
    return Services.objects.all()
def get_customers_job(customer_code):
    # Müşteri bilgisini almak
    customer = get_object_or_404(Customer, code=customer_code)
    
    # Müşterinin iş bilgisini almak (örneğin, `CustomerJob` modeli varsa)
    customer_job = Job.objects.filter(customer=customer)
    
    return customer_job
def get_customer_payment(customer_code):
    # Müşteri bilgisini almak
    customer = get_object_or_404(Customer, code=customer_code)
    
    # Müşterinin iş bilgisini almak (örneğin, `CustomerJob` modeli varsa)
    payments = Payment.objects.filter(customer=customer)
    return payments
# Ekleme Alanları
def add_customer(request):
    if request.method != "POST":
        messages.error(request, "Geçersiz istek yöntemi")
        return redirect("dashboard")

    customerform = CustomerForm(request.POST, request=request)  # Pass the request object

    if not customerform.is_valid():
        messages.error(request, "Lütfen formu doğru doldurun. Hatalar: " + str(customerform.errors))
        return redirect("dashboard")

    customerform.save()  # Save the form (created_by is automatically set)
    messages.success(request, "Müşteri başarıyla eklendi")
    return redirect("dashboard")
def all_customers(request):
    customers = get_customers()
    context = {
        'customers':customers,
    }
    return render(request,"customers.html",context)
def customer_detail(request, customer_code):
    # Müşteri bilgisini almak
    customer = get_object_or_404(Customer, code=customer_code)
    
    # get_customers_job fonksiyonunu kullanarak iş bilgisini almak
    customer_jobs = get_customers_job(customer_code)
    customer_payments = get_customer_payment(customer_code)
    # Context verisini oluşturma
    context = {
        'customer': customer,
        'customer_jobs': customer_jobs,  # Müşterinin iş bilgilerini de ekliyoruz
        'customer_payments':customer_payments,
    }
    
    return render(request, 'customer_detail.html', context)
def add_employee_page(request):
    services = get_services()
    employees= get_employee()
    employee_form = EmployeeForm()
    service_form = ServiceForm()
    context = {
        "services":services,
        "service_form":service_form,
        "employees": employees,
        "employee_form": employee_form,
    }
    return render(request, "add_employee_page.html", context)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


@csrf_exempt  # CSRF hatalarını geçici olarak geçmek için
@csrf_exempt  # CSRF koruması için dekoratör
@csrf_exempt
@csrf_exempt

def update_employee_status(request, employee_id):
    try:
        # JSON verisini al
        data = json.loads(request.body)
        is_active = data.get('is_active', None)

        if is_active is None:
            return JsonResponse({'success': False, 'message': 'Geçersiz veri.'}, status=400)

        # Kullanıcıyı al
        employee = User.objects.get(id=employee_id)
        
        # Durumu güncelle
        employee.is_active = is_active
        employee.save()

        return JsonResponse({'success': True})

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Çalışan bulunamadı.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Geçersiz JSON verisi.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
def add_employee(request):
    if request.method != "POST":
        messages.error(request, "Geçersiz istek yöntemi")
        return redirect("add_employee_page")

    employeeform = EmployeeForm(request.POST)

    if not employeeform.is_valid():
        print(employeeform.errors)
        messages.error(request, "Lütfen formu doğru doldurun. Hatalar: " + str(employeeform.errors))
        return redirect("add_employee_page")

    employeeform.save()
    messages.success(request, "Kullanıcı başarıyla eklendi")
    return redirect("add_employee_page")
def add_service(request):
    if request.method != "POST":
        messages.error(request, "Geçersiz istek yöntemi")
        return redirect("add_employee_page")

    serviceform = ServiceForm(request.POST)
    if not serviceform.is_valid():
        print(serviceform.errors)
        messages.error(request, "Lütfen formu doğru doldurun. Hatalar: " + str(serviceform.errors))
        return redirect("add_employee_page")

    service = serviceform.save(commit=False)  # Veritabanına kaydetmeden önce nesneyi al
    service.created_by = request.user  # Oturum açmış kullanıcıyı atayın
    service.save()  # Şimdi kaydedin

    messages.success(request, "Servis başarıyla eklendi")
    return redirect("add_employee_page")

def update_service_status(request, service_id):
    if request.method == 'POST':
        # Servis durumu güncelleniyor
        try:
            service = Services.objects.get(id=service_id)
            is_active = request.POST.get('is_active') == 'true'
            service.is_active = is_active
            service.save()
            return JsonResponse({'success': True})
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Servis bulunamadı.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'}, status=400)
from django.http import JsonResponse
# iş ile ilgil alanlar
def get_all_jobs(user_id=None):
    if user_id:
        return Job.objects.filter(employee_id=user_id)
    return Job.objects.all()
def add_job_page(request):
    job_form = JobForm()
    context = {

        "job_form": job_form,
    }
    return render(request, "add_job_page.html", context)
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            # created_by alanını, oturumdaki kullanıcı ile ilişkilendiriyoruz
            job = form.save(commit=False)
            job.created_by = request.user  # Burada created_by alanını oturumdaki kullanıcı ile set ediyoruz
            job.save()
            return redirect('job_list')  # Başarılı kaydeden sonra yönlendirme yapılabilir
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})
def my_job_list(request):
    user_id = request.user.id  # Oturum açan kullanıcının ID'sini al
    jobs = get_all_jobs(user_id)
    context = {
        'jobs': jobs,
    }
    return render(request, 'my_job_list.html', context)
def all_job_list(request):
    jobs=get_all_jobs()
    context = {
        'jobs':jobs,
    }
    return render(request,'all_job_list.html',context)
def list_job_page(request):
    jobs = get_all_jobs()
    return render(request, 'job_list.html', {'jobs': jobs})
def job_detail(request,job_id):
    job = get_object_or_404(Job,id=job_id)
    context = {
        'job':job,
    }
    return render(request,'job_detail.html',context) 

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Job

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Job

def job_status_update(request):
    if request.method == 'POST' and request.user.is_authenticated:
        job_id = request.POST.get('job_id')
        status = request.POST.get('status')
        print(job_id)
        print(status)

        try:
            # Try to get the Job object
            job = get_object_or_404(Job, id=job_id)
            print(job)

            # Fetch customer linked to this job for reuse
            customer = job.customer

            # If the job is already in the requested status, do not make any changes
            if job.status == status:
                status_display = dict(Job.STATUS_CHOICES).get(status, status)
                return JsonResponse({'error': f'İş zaten {status_display} durumunda.'}, status=400)

            # Check if the current job status is in-progress or completed and user trying to set it to 'pending'
            if job.status == status:
                return JsonResponse({'error': 'Bu iş zaten işlemde veya tamamlandı. Beklemeye alınamaz.'}, status=400)

            # If the status is 'pending', reset end_date
            if status == 'pending':
                job.end_date = None

            # If the status is 'completed', update the end date and customer balance
            elif status == 'completed':
                job.end_date = timezone.now()  # Set the current time as end date
                customer.balance += job.total_price  # Increase balance with job's total price
                customer.save()  # Save updated customer balance

            # If the status is 'cancelled', adjust the balance as needed
            elif status == 'cancelled':
                job.end_date = timezone.now()  # Set the current time as end date on cancellation
                customer.balance -= job.total_price  # Deduct job's total price from balance
                customer.save()  # Save updated customer balance

            # If the status is 'in_progress', reset end_date and reduce the balance
            elif status == 'in_progress':
                job.end_date = None  # Reset end date if job is moved to in-progress
                customer.balance -= job.total_price  # Deduct job's total price from balance
                customer.save()

            # Update job status
            job.status = status
            job.save()

            # Send back the updated information
            end_date = job.end_date.strftime('%Y-%m-%d %H:%M:%S') if job.end_date else None
            return JsonResponse({
                'success': True,
                'status': job.status,  # Current job status
                'end_date': end_date,  # End date formatted
                'job_id': job.id,  # Job ID
                'customer_balance': customer.balance  # Updated customer balance
            })

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'İş bulunamadı.'}, status=404)

        except Exception as e:
            # Catch any other unexpected errors
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST or user is not authenticated
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)
# iş ile ilgil alanlar
def get_service_price(request):
    service_id = request.GET.get("service_id")
    service = Services.objects.filter(id=service_id).first()
    if service:
        return JsonResponse({"price": float(service.price) if service.price else 0})
    return JsonResponse({"price": 0})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Customer, Payment  # Customer ve Payment modelini import ettiğinizden emin olun

from decimal import Decimal

from decimal import Decimal
from django.db.models import Sum

def payment(request, customer_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # Müşteri bilgilerini alıyoruz
            customer = get_object_or_404(Customer, id=customer_id)
            amount = request.POST.get('amount')
            payment_method = request.POST.get('payment_method')
            
            if not amount or not payment_method:
                return JsonResponse({'error': 'Ödeme tutarı ve ödeme yöntemi gereklidir.'}, status=400)

            # amount'ı Decimal'e dönüştürme
            amount = Decimal(amount)
            
            # Ödeme işlemi oluşturuluyor
            payment = Payment(
                customer=customer,
                amount=amount,
                payment_method=payment_method,
                payment_date=timezone.now(),
            )
            payment.save()

            # Müşterinin bakiyesi güncelleniyor
            customer.balance -= amount  # Bakiyeyi güncelliyoruz
            customer.save()

            # Müşterinin toplam ödemelerini topluyoruz
            total_paid = Payment.objects.filter(customer=customer).aggregate(total_paid=Sum('amount'))['total_paid'] or Decimal('0.00')

            # `paid` alanını güncelliyoruz
            customer.paid = total_paid
            customer.save()

            return JsonResponse({
                'success': True,
                'message': 'Ödeme başarılı bir şekilde alındı.',
                'payment_id': payment.id,
                'new_balance': customer.balance,
                'total_paid': customer.paid,
            })

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Müşteri bulunamadı.'}, status=404)

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)



    
# login and logout 
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
# report
from django.shortcuts import render
from .models import Job, Services

def most_transactions_report(request):
    # Servislere göre yapılan işler
    services = Services.objects.all()
    service_data = []
    
    for service in services:
        # Her servis için yapılmış işlerin sayısını hesaplıyoruz
        job_count = Job.objects.filter(service=service).count()
        
        # Servis adı ve iş sayısını saklıyoruz
        service_data.append({
            'service_name': service.name,
            'job_count': job_count
        })

    # Bu veriyi raporda kullanmak üzere template'e gönderiyoruz
    return render(request, 'reports/most_transactions_report.html', {'service_data': service_data})
from django.utils.timezone import now
from datetime import timedelta

from django.utils.timezone import now
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from .models import Job

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from .models import Job

from datetime import timedelta, datetime

from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from .models import Job  # Job modelinizi içeri aktarın

from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Job

from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Job  # Assuming your Job model is imported from the correct module

from datetime import datetime, timedelta

from datetime import datetime, timedelta
from django.http import JsonResponse

import pytz
from datetime import datetime, timedelta
from django.http import JsonResponse

def job_events(request):
    local_tz = pytz.timezone("Europe/Istanbul")  # Türkiye saat dilimi
    jobs = Job.objects.all()
    events = []

    for job in jobs:
        if job.appointment_date and job.appointment_time:
            # appointment_date ve appointment_time birleştiriliyor
            start_time = datetime.combine(job.appointment_date, job.appointment_time)

            # Eğer start_time'da bir zaman dilimi yoksa, yerel saat dilimi ekliyoruz
            if start_time.tzinfo is None:
                start_time = local_tz.localize(start_time)  # Yerel saate çevir

            end_time = start_time + timedelta(hours=1)  # 1 saat sonrası
            # End time'ı da yerel saat dilimine çevirebiliriz
            end_time = start_time + timedelta(hours=1)
            end_time = end_time.astimezone(local_tz)
        else:
            start_time = end_time = None

        events.append({
            'id': job.id,
            'title': f"{job.customer.brand_name} - {job.service.name}",
            'start': start_time.strftime("%Y-%m-%dT%H:%M:%S") if start_time else None,
            'end': end_time.strftime("%Y-%m-%dT%H:%M:%S") if end_time else None,
            'description': job.info,
            'status': job.status,
            'color': get_status_color(job.status),
        })
    
    return JsonResponse(events, safe=False)

from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Job
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import pytz
from .models import Job
@csrf_exempt
@csrf_exempt
def update_job_event(request):
    if request.method == "POST":
        try:
            print("API çağrıldı!")  # API çağrıldığını kontrol et

            data = json.loads(request.body)
            job = Job.objects.get(id=data['id'])

            # Django'daki TIME_ZONE ayarını kullanarak yerel saat dilimini belirle
            local_tz = pytz.timezone("Europe/Istanbul")  # Türkiye saat dilimi
            new_start_utc = datetime.fromisoformat(data['start']).replace(tzinfo=pytz.utc)  # UTC olarak al
            new_start_local = new_start_utc.astimezone(local_tz)  # Türkiye saatine çevir

            new_date = new_start_local.date()
            new_time = new_start_local.time()

            print('Yeni Tarih:', new_date)  # Güncel tarihi yazdır
            print('Yeni Zaman:', new_time)  # Saatin doğru kaydedildiğini kontrol et

            job.appointment_date = new_date
            job.appointment_time = new_time
            job.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Hata:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def get_status_color(status):
    colors = {
        'pending': 'orange',
        'in_progress': 'blue',
        'completed': 'green',
        'cancelled': 'red',
    }
    return colors.get(status, 'gray')


def upcoming_appointments_report_page(request):
    return render(request, 'reports/upcoming_appointments_report.html')  # Render the report page template

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job

@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        start_time = request.POST.get('start')
        end_time = request.POST.get('end')

        try:
            # Etkinliği ID'ye göre buluyoruz
            job = Job.objects.get(id=event_id)
            job.appointment_date = start_time[:10]  # Tarih kısmını alıyoruz
            job.appointment_time = start_time[11:]  # Saat kısmını alıyoruz
            job.save()

            # Etkinliği güncelledikten sonra başarılı yanıt gönderiyoruz
            return JsonResponse({'status': 'success'}, status=200)
        except Job.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Etkinlik bulunamadı.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'}, status=400)

def login_view(request):
    if request.method != "POST":
        return render(request, 'login.html')
    
    username = request.POST.get("username")
    
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        auth_login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'login.html', {'error': 'Invalid login credentials'})
