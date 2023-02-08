from django.contrib import admin
from django.urls import path,include,re_path
from accounts import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from profiles import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('profiles/', include("profiles.urls")),
    path('',views.home),
]


