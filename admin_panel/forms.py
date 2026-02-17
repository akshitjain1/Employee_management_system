from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# form for creating employees
class EmployeeCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    phone = forms.CharField(max_length=15, required=True)
    department = forms.CharField(max_length=100, required=True)
    salary = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'role', 'department', 'salary', 'date_of_joining']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('HR', 'HR'), ('Employee', 'Employee')]

# form for editing employees
class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'salary', 'date_of_joining', 'is_active']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

# change password form
class ChangePasswordForm(forms.Form):
    otp_code = forms.CharField(max_length=6, required=True, label='OTP Code')
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')
    
    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get('new_password')
        confirm_pass = cleaned_data.get('confirm_password')
        
        if new_pass and confirm_pass and new_pass != confirm_pass:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
