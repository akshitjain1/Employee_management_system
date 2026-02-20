from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'Employee':
            messages.error(request, "Access denied. This page is only for employees")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@employee_required
def employee_profile(request):
    """Employee profile view and edit"""
    from users.forms import ProfileEditForm
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employee:employee_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'employee_module/profile.html', {
        'form': form,
        'user': request.user
    })
