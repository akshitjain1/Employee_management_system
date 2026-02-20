from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('quote/', views.quote, name='quote'),
    path('services/application-development/', views.application_development, name='application_development'),
    path('services/web-development/', views.web_development, name='web_development'),
    path('services/cms-ecommerce/', views.cms_ecommerce, name='cms_ecommerce'),
    path('services/digital-marketing/', views.digital_marketing, name='digital_marketing'),
    path('services/website-designing/', views.website_designing, name='website_designing'),
    path('services/mobile-applications/', views.mobile_applications, name='mobile_applications'),
]
