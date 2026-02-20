from django.shortcuts import render, redirect

def home(request):
    """Home page view"""
    return render(request, 'home/home.html')

def about(request):
    """About page view"""
    return render(request, 'home/about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'home/contact.html')

def quote(request):
    """Request a quote page view"""
    return render(request, 'home/quote.html')

def application_development(request):
    """Application Development service page"""
    return render(request, 'home/services/application_development.html')

def web_development(request):
    """Web Development service page"""
    return render(request, 'home/services/web_development.html')

def cms_ecommerce(request):
    """CMS & E-Commerce service page"""
    return render(request, 'home/services/cms_ecommerce.html')

def digital_marketing(request):
    """Digital Marketing service page"""
    return render(request, 'home/services/digital_marketing.html')

def website_designing(request):
    """Website Designing service page"""
    return render(request, 'home/services/website_designing.html')

def mobile_applications(request):
    """Mobile Applications service page"""
    return render(request, 'home/services/mobile_applications.html')
