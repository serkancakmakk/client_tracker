import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta

# Django projesini tanıt
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "client_tracker.settings")  # Projeye göre değiştir
django.setup()

# Modelleri içe aktar
from tracking.models import User, Customer, Services, Job, Payment  # Uygulama adını değiştir

fake = Faker()

# 1️⃣ Kullanıcıları Oluştur
users = []
for _ in range(10):
    user = User.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        username=fake.unique.user_name(),  # Kullanıcı adı benzersiz olacak şekilde oluşturuluyor
        email=fake.unique.email(),
        phone=fake.phone_number(),
        is_active=True
    )
    users.append(user)

# 2️⃣ Müşterileri Oluştur
customers = []
for _ in range(10):
    customer = Customer.objects.create(
        code = fake.unique.random_number(digits=6, fix_len=True), # Örneğin: 785412
        owner_name=fake.first_name(),
        owner_surname=fake.last_name(),
        brand_name=fake.company(),
        address=fake.address(),
        phone=fake.phone_number(),
        email=fake.unique.email(),
        created_by=random.choice(users)
    )
    customers.append(customer)

# 3️⃣ Hizmetleri Oluştur
services = []
for _ in range(10):
    service = Services.objects.create(
        name=fake.word(),
        created_by=random.choice(users),
        price=round(random.uniform(100, 1000), 2),
        is_active=True
    )
    services.append(service)

# 4️⃣ İşleri (Job) Oluştur
jobs = []
for _ in range(10):
    job = Job.objects.create(
        employee=random.choice(users),
        customer=random.choice(customers),
        service=random.choice(services),
        price=round(random.uniform(100, 1000), 2),
        vat=random.randint(5, 20),
        total_price=round(random.uniform(120, 1500), 2),
        info=fake.sentence(),
        created_date=fake.date_time_this_year(),
        end_date=fake.date_time_this_year(),
        appointment_date=fake.date_this_year(),
        appointment_time=fake.time_object(),
        created_by=random.choice(users),
        status=random.choice(['pending', 'in_progress', 'completed', 'cancelled', 'awaited'])
    )
    jobs.append(job)

# 5️⃣ Ödeme (Payment) Oluştur
for _ in range(10):
    Payment.objects.create(
        customer=random.choice(customers),
        amount=round(random.uniform(50, 2000), 2),
        payment_method=random.choice(['Credit Card', 'Cash', 'Bank Transfer']),
        payment_date=fake.date_time_this_year()
    )

print("✅ Fake data başarıyla oluşturuldu!")
