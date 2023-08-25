from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin 
from django.urls import path, include


app_name = 'djangoapp'
urlpatterns = [
    path('about/', views.about, name='about'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration_request, name='registration'),
    path('car_make_list/', views.car_make_list, name='car_make_list'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('car_model_list/<int:car_make_id>/', views.car_model_list, name='car_model_list'),
    path(route='', view=views.get_dealerships, name='index'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 

    # path for dealer reviews view

    # path for add a review view



 

    # path for dealer reviews view

    # path for add a review view

