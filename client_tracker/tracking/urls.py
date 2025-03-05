from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard,name="dashboard"),
    # customer
    path("add_customer", views.add_customer,name="add_customer"),
    # employee
    path("add_employee_page", views.add_employee_page,name="add_employee_page"),
    # add employee
    path("add_employee", views.add_employee,name="add_employee"),
     # add service
    path("add_service", views.add_service,name="add_service"),
    # add job
    path("add_job_page", views.add_job_page,name="add_job_page"),
    path("add_job",views.add_job,name="add_job"),
    path("list_job",views.list_job_page,name="list_job"),
    path("job_detail/<int:job_id>/",views.job_detail,name="job_detail"),
    path('job/status/update/', views.job_status_update, name='job_status_update'),
    path('job_list/', views.all_job_list, name='job_list'),
    path('my_job_list/', views.my_job_list, name='my_job_list'),
    # endpoint
    path("get-service-price/", views.get_service_price, name="get_service_price"),
    
    path("login",views.login_view,name="login_view"),
]