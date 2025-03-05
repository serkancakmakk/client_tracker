from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomerForm, EmployeeForm, JobForm, ServiceForm
from .models import Customer, Job, Services, User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

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

def job_status_update(request):
    if request.method == 'POST' and request.user.is_authenticated:
        job_id = request.POST.get('job_id')
        status = request.POST.get('status')

        # Job objesini al
        job = get_object_or_404(Job, id=job_id)

        # Eğer kullanıcı bu işin employee'si ise, durumu güncelleyebilir
        if job.employee == request.user:
            print(status)
            job.status = status
            print(job.status)
            # Eğer iş tamamlanmışsa, end_date'i güncelle
            if status == 'completed':
                job.end_date = timezone.now()
            elif status == 'in_progress':
                job.end_date = None  # İş yeniden işleme alındığında end_date sıfırlanır

            job.save()

            # `end_date`'yi frontend'e doğru formatta döndürüyoruz
            end_date = job.end_date.strftime('%Y-%m-%d %H:%M:%S') if job.end_date else None

            return JsonResponse({
                'success': True,
                'status': job.status,  # Durum bilgisi
                'end_date': end_date,  # Bitiş tarihi
                'job_id': job.id  # Job ID'yi de döndürüyoruz
            })

        else:
            return JsonResponse({'error': 'Bu işlemi yapmaya yetkiniz yok.'}, status=403)

    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)
# iş ile ilgil alanlar
def get_service_price(request):
    service_id = request.GET.get("service_id")
    service = Services.objects.filter(id=service_id).first()
    if service:
        return JsonResponse({"price": float(service.price) if service.price else 0})
    return JsonResponse({"price": 0})


# login and logout 
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

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
