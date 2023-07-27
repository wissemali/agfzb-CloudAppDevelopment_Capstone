from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin 
from django.urls import path, include


app_name = 'djangoapp'
urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration_request, name='registration'),
    path(route='', view=views.get_dealerships, name='index'),
  

 

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)