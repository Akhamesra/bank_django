from django.urls import path
from . import views
app_name ="restful_api"
urlpatterns = [
    path('show_details',views.show_details,name = 'show_details'),
    path(r"account_management", views.account_management, name='account_management'),
    path(r"stat_gen", views.stat_gen, name='stat_gen'),

]