from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('launch_vm_request',views.launch_vm_request,name='launch_vm'),
    path('launch_vm_request/new_vm',views.new_vm, name='new_vm'),
    path('manage_vm/power_on',views.power_on, name='power_on'),
    path('manage_vm/power_off',views.power_off, name='power_off'),
    path('manage_vm/restart',views.restart, name='restart'),
    path('manage_vm/user_add',views.user_add,name='user_add'),
    path('manage_vm/user_remove',views.user_remove,name='user_remove'),
    path('manage_vm/create_dir',views.create_dir,name='create_dir'),
    path('manage_vm/delete_dir',views.delete_dir,name='delete_dir'),
    path('open-exercise/<int:exercise_id>/',views.open_pdf,name='open-exercise'),
]