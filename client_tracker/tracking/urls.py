from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.dashboard,name="dashboard"),
    # customer
    path("add_customer", views.add_customer,name="add_customer"),
    path("list_customers",views.all_customers,name="list_customers"),
    path("customer_detail/<int:customer_code>",views.customer_detail,name="customer_detail"),
    path("payment/<int:customer_id>",views.payment,name="payment"),
    # employee
    path("add_employee_page", views.add_employee_page,name="add_employee_page"),
    path("add_employee", views.add_employee,name="add_employee"),
    path('update_employee_status/<int:employee_id>/', views.update_employee_status, name='update_employee_status'),
     # add service
    path("add_service", views.add_service,name="add_service"),
    # change service
    path('update_service_status/<int:service_id>/', views.update_service_status, name='update_service_status'),    # add job
    path("add_job_page", views.add_job_page,name="add_job_page"),
    path("add_job",views.add_job,name="add_job"),
    path("list_job",views.list_job_page,name="list_job"),
    path("job_detail/<int:job_id>/",views.job_detail,name="job_detail"),
    path('job/status/update/', views.job_status_update, name='job_status_update'),
    path('job_list/', views.all_job_list, name='job_list'),
    path('my_job_list/', views.my_job_list, name='my_job_list'),
    # endpoint
    path("get-service-price/", views.get_service_price, name="get_service_price"),
    #report
    path("most_transactions_report/", views.most_transactions_report, name="most_transactions_report"),
    path('api/job-events/', views.job_events, name='job_events'),
    path('upcoming_appointments_report_page/', views.upcoming_appointments_report_page, name='upcoming_appointments_report_page'),
    path('update_event/', views.update_event, name='update_event'),
    path('api/update-job-event/', views.update_job_event, name='update_job_event'),  # Sürükleme sonrası güncelleme API
    path("logout",views.logout_view,name="logout_view"),
    path("login",views.login_view,name="login_view"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)