
from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('home',views.home,name='home'),
    path('user_details',views.user_details,name = 'user_details'),
    path('show_details',views.show_details,name = 'show_details'),
    path("dashboard", views.display_menu, name = "dashboard"),
    path("redirect_from_dashboard", views.get_function_chosen, name = "get_function_chosen"),
    path("account_management", views.account_management, name='account_management'),
    path("process_account_action", views.get_account_action, name='get_account_action'),
    path("withdraw", views.withdraw, name='withdraw'),
    path("deposit", views.deposit, name='deposit'),
    path("stat_gen", views.stat_gen, name='stat_gen'),
    path("get_stat_gen", views.get_transaction_action, name='get_transaction_action'),
    path('admin_view', views.admin_view, name="admin_view"),
    path('transfer', views.transfer, name="transfer"),
    path('error', views.error, name = 'error')
]

