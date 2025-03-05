from .models import Job  # Kullanıcıya ait işlerin bulunduğu model
from django.utils import timezone
from django.shortcuts import render
from .models import Job


def user_jobs(request):
    if request.user.is_authenticated:
        tasks = Job.objects.filter(
            employee=request.user,
            status="pending",
            appointment_date__date=timezone.now().date()  # Bugün olan işler
        )
        print(tasks.count())
    else:
        tasks = []
    
    return {
        'user_jobs': tasks  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }

def all_jobs(request):
    if request.user.is_authenticated:
        all_jobs = Job.objects.filter(status="pending",
            appointment_date__date=timezone.now().date())  # Kullanıcının işlerini al
        print(all_jobs.count)
    else:
        all_jobs = []
    
    return {
        'all_jobs': all_jobs  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }


def my_future_works(request):
    if request.user.is_authenticated:
        my_future_works = Job.objects.filter(
            status="pending",
            appointment_date__gt=timezone.now()  # Bugünden ileri tarihli işler
        )
    else:
        my_future_works = []
    
    return {
        'my_future_works': my_future_works  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }

