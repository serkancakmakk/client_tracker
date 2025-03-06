from django.utils import timezone

from .models import Job

# Bugün olan işler
def user_jobs(request):
    if request.user.is_authenticated:
        today = timezone.localtime(timezone.now()).date()  # Bugün tarihini yerel zamanla al
        tasks = Job.objects.filter(
            employee=request.user,
            status="pending",
            appointment_date__year=today.year,  # Yıl bazında filtreleme
            appointment_date__month=today.month,  # Ay bazında filtreleme
            appointment_date__day=today.day  # Gün bazında filtreleme
        )
        print(tasks.count())
    else:
        tasks = []
    
    return {
        'user_jobs': tasks  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }

# Tüm pending işler
def all_jobs(request):
    if request.user.is_authenticated:
        today = timezone.localtime(timezone.now()).date()  # Bugün tarihini yerel zamanla al
        all_jobs = Job.objects.filter(
            status="pending",
            appointment_date__year=today.year,
            appointment_date__month=today.month,
            appointment_date__day=today.day
        )
        print(all_jobs.count())
    else:
        all_jobs = []
    
    return {
        'all_jobs': all_jobs  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }

# Bugünden ileri tarihli işler
def my_future_works(request):
    if request.user.is_authenticated:
        my_future_works = Job.objects.filter(
            status="pending",
            appointment_date__gt=timezone.localtime(timezone.now())  # Bugünden ileri tarihli işler
        )
    else:
        my_future_works = []
    
    return {
        'my_future_works': my_future_works  # Context'e ekleyerek tüm şablonlarda kullanılmasını sağla
    }
